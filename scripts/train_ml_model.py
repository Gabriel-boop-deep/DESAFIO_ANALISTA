#!/usr/bin/env python3
"""Train simple and interpretable ML assets on top of mart_performance_tmae."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
KEYFILE = PROJECT_ROOT / "desafio-analista-499820-978397414cd8.json"
PROJECT_ID = "desafio-analista-499820"
DATASET_ID = "dbt_desafio_analista"
SOURCE_TABLE = f"{PROJECT_ID}.{DATASET_ID}.mart_performance_tmae"
TARGET_TABLE = f"{PROJECT_ID}.{DATASET_ID}.ml_tmae_resultados"


def build_client() -> bigquery.Client:
    credentials = service_account.Credentials.from_service_account_file(KEYFILE)
    return bigquery.Client(project=PROJECT_ID, credentials=credentials)


def load_source_dataframe(client: bigquery.Client) -> pd.DataFrame:
    query = f"""
        select
            data_referencia,
            distribuidora,
            regiao,
            grupo_economico,
            tmp,
            tmd,
            tme,
            tmae,
            quantidade_ocorrencias,
            media_tmae_brasil,
            variacao_abs_mes_anterior,
            variacao_pct_mes_anterior,
            tendencia,
            principal_componente_tmae,
            flag_neoenergia_coelba
        from `{SOURCE_TABLE}`
        where tmae is not null
    """
    dataframe = client.query(query).to_dataframe()
    dataframe["data_referencia"] = pd.to_datetime(dataframe["data_referencia"])
    return dataframe.sort_values(["distribuidora", "data_referencia"]).reset_index(drop=True)


def add_anomaly_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    feature_columns = [
        "tmae",
        "tmp",
        "tmd",
        "tme",
        "quantidade_ocorrencias",
        "variacao_abs_mes_anterior",
    ]
    filled = dataframe[feature_columns].fillna(0.0)
    isolation_forest = IsolationForest(
        contamination=0.05,
        random_state=42,
    )
    dataframe["score_anomalia"] = -isolation_forest.fit(filled).score_samples(filled)
    threshold = dataframe["score_anomalia"].quantile(0.95)
    dataframe["flag_anomalia"] = dataframe["score_anomalia"] >= threshold
    return dataframe


def build_cluster_reference(dataframe: pd.DataFrame) -> pd.DataFrame:
    aggregated = (
        dataframe.groupby("distribuidora", as_index=False)
        .agg(
            tmae_medio=("tmae", "mean"),
            tmae_std=("tmae", "std"),
            tmp_medio=("tmp", "mean"),
            tmd_medio=("tmd", "mean"),
            tme_medio=("tme", "mean"),
            variacao_media_tmae=("variacao_abs_mes_anterior", "mean"),
            quantidade_media_ocorrencias=("quantidade_ocorrencias", "mean"),
            percentual_meses_pior_que_brasil=(
                "tmae",
                lambda values: np.nan,
            ),
        )
    )

    pior_que_brasil = (
        dataframe.assign(pior_que_brasil=dataframe["tmae"] > dataframe["media_tmae_brasil"])
        .groupby("distribuidora", as_index=False)["pior_que_brasil"]
        .mean()
        .rename(columns={"pior_que_brasil": "percentual_meses_pior_que_brasil"})
    )
    aggregated = aggregated.drop(columns=["percentual_meses_pior_que_brasil"]).merge(
        pior_que_brasil, on="distribuidora", how="left"
    )

    feature_columns = [
        "tmae_medio",
        "tmae_std",
        "tmp_medio",
        "tmd_medio",
        "tme_medio",
        "variacao_media_tmae",
        "quantidade_media_ocorrencias",
        "percentual_meses_pior_que_brasil",
    ]
    filled = aggregated[feature_columns].fillna(0.0)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(filled)
    kmeans = KMeans(n_clusters=4, n_init=20, random_state=42)
    aggregated["cluster_performance"] = kmeans.fit_predict(scaled).astype(str)

    cluster_stats = (
        aggregated.groupby("cluster_performance", as_index=False)
        .agg(tmae_medio=("tmae_medio", "mean"), tmae_std=("tmae_std", "mean"))
        .sort_values(["tmae_medio", "tmae_std"])
        .reset_index(drop=True)
    )
    labels = [
        "Alta eficiencia e baixa volatilidade",
        "Eficiencia intermediaria",
        "Atencao operacional",
        "Alto tempo medio e alta volatilidade",
    ]
    cluster_stats["interpretacao_cluster"] = labels[: len(cluster_stats)]
    return aggregated.merge(
        cluster_stats[["cluster_performance", "interpretacao_cluster"]],
        on="cluster_performance",
        how="left",
    )


def add_forecast(dataframe: pd.DataFrame) -> pd.DataFrame:
    predictions: list[pd.DataFrame] = []
    for distribuidora, group in dataframe.groupby("distribuidora"):
        ordered = group.sort_values("data_referencia").copy()
        ordered["indice_tempo"] = np.arange(len(ordered), dtype=float)
        if len(ordered) >= 2:
            model = LinearRegression()
            model.fit(ordered[["indice_tempo"]], ordered["tmae"])
            ordered["tmae_previsto"] = model.predict(ordered[["indice_tempo"]])
            ordered["tendencia_prevista"] = np.where(
                model.coef_[0] < -0.01,
                "Melhora",
                np.where(model.coef_[0] > 0.01, "Piora", "Estavel"),
            )
        else:
            ordered["tmae_previsto"] = ordered["tmae"]
            ordered["tendencia_prevista"] = "Estavel"
        predictions.append(ordered)
    result = pd.concat(predictions, ignore_index=True)
    result["erro_previsao"] = result["tmae"] - result["tmae_previsto"]
    return result


def add_recommendations(dataframe: pd.DataFrame) -> pd.DataFrame:
    conditions = [
        dataframe["flag_anomalia"],
        dataframe["principal_componente_tmae"].eq("Deslocamento"),
        dataframe["tendencia_prevista"].eq("Piora"),
        dataframe["cluster_performance"].isin(["2", "3"]),
    ]
    choices = [
        "Investigar meses anomalos e revisar causas operacionais.",
        "Analisar componente TMD e rotas de deslocamento.",
        "Monitorar tendencia de piora e reforcar plano de contingencia.",
        "Comparar com benchmarks do mesmo cluster e priorizar plano corretivo.",
    ]
    dataframe["recomendacao_negocio"] = np.select(
        conditions,
        choices,
        default="Manter monitoramento e comparar com benchmark nacional.",
    )
    return dataframe


def persist_results(client: bigquery.Client, dataframe: pd.DataFrame) -> None:
    output = dataframe[
        [
            "distribuidora",
            "data_referencia",
            "tmae",
            "tmae_previsto",
            "erro_previsao",
            "score_anomalia",
            "flag_anomalia",
            "cluster_performance",
            "interpretacao_cluster",
            "tendencia_prevista",
            "recomendacao_negocio",
        ]
    ].copy()

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(output, TARGET_TABLE, job_config=job_config)
    job.result()


def main() -> None:
    client = build_client()
    dataframe = load_source_dataframe(client)
    dataframe = add_anomaly_features(dataframe)
    cluster_reference = build_cluster_reference(dataframe)
    dataframe = dataframe.merge(
        cluster_reference[
            ["distribuidora", "cluster_performance", "interpretacao_cluster"]
        ],
        on="distribuidora",
        how="left",
    )
    dataframe = add_forecast(dataframe)
    dataframe = add_recommendations(dataframe)
    persist_results(client, dataframe)

    print(f"Resultados gravados em {TARGET_TABLE}")
    print(f"Linhas processadas: {len(dataframe)}")


if __name__ == "__main__":
    main()

