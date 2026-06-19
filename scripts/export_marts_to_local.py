#!/usr/bin/env python3
"""Exporta as tabelas analiticas do BigQuery para arquivos locais Parquet."""

from __future__ import annotations

from pathlib import Path

from google.cloud import bigquery
from google.oauth2 import service_account


PROJECT_ROOT = Path(__file__).resolve().parents[1]
KEYFILE = PROJECT_ROOT / "desafio-analista-499820-978397414cd8.json"
PROJECT_ID = "desafio-analista-499820"
OUTPUT_DIR = PROJECT_ROOT / "data" / "offline"
TABLES = {
    "mart_performance_tmae": "dbt_desafio_analista_marts",
    "mart_coelba_tmae": "dbt_desafio_analista_marts",
    "mart_ranking_distribuidoras": "dbt_desafio_analista_marts",
    "mart_componentes_tmae": "dbt_desafio_analista_marts",
    "mart_ml_features_tmae": "dbt_desafio_analista_marts",
    "ml_tmae_resultados": "dbt_desafio_analista_marts",
    "dim_tempo": "dbt_desafio_analista_dimensions",
    "dim_distribuidora": "dbt_desafio_analista_dimensions",
}


def build_client() -> bigquery.Client:
    credentials = service_account.Credentials.from_service_account_file(KEYFILE)
    return bigquery.Client(project=PROJECT_ID, credentials=credentials)


def main() -> None:
    client = build_client()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for table_name, dataset_name in TABLES.items():
        query = f"select * from `{PROJECT_ID}.{dataset_name}.{table_name}`"
        dataframe = client.query(query).to_dataframe()
        output_path = OUTPUT_DIR / f"{table_name}.parquet"
        dataframe.to_parquet(output_path, index=False)
        print(f"{table_name}: {len(dataframe)} linhas exportadas para {output_path}")


if __name__ == "__main__":
    main()
