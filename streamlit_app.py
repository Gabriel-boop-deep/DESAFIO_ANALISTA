from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from google.api_core.exceptions import NotFound
from google.cloud import bigquery
from google.oauth2 import service_account


PROJECT_ID = "desafio-analista-499820"
PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_KEYFILE = PROJECT_ROOT / "desafio-analista-499820-978397414cd8.json"
LOCAL_DATA_DIR = PROJECT_ROOT / "data" / "offline"
COLOR_PRIMARY = "#003F7D"
COLOR_GREEN = "#00A651"
COLOR_GREEN_SOFT = "#34B233"
COLOR_BLUE_SOFT = "#00B5E2"
COLOR_WARNING = "#F28C28"
COLOR_DANGER = "#D94F4F"
COLOR_TEXT = "#1F2D3D"
COLOR_MUTED = "#486581"
COLOR_BG = "#F5F8FB"
COLOR_CARD = "#FFFFFF"


st.set_page_config(
    page_title="Neoenergia Coelba | TMAE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(180deg, #f5f8fb 0%, #eef4f8 100%);
        }}
        .hero {{
            padding: 1.4rem 1.6rem;
            background: linear-gradient(135deg, {COLOR_PRIMARY} 0%, #0059a8 100%);
            border-radius: 18px;
            color: white;
            margin-bottom: 1rem;
            box-shadow: 0 16px 40px rgba(0, 63, 125, 0.18);
        }}
        .hero h1 {{
            margin: 0;
            font-size: 2rem;
        }}
        .hero p {{
            margin: 0.35rem 0 0 0;
            color: rgba(255,255,255,0.88);
        }}
        .metric-card {{
            background: {COLOR_CARD};
            border: 1px solid #d9e2ec;
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
            min-height: 124px;
        }}
        .metric-label {{
            font-size: 0.86rem;
            color: {COLOR_MUTED};
            margin-bottom: 0.45rem;
        }}
        .metric-value {{
            font-size: 1.9rem;
            font-weight: 700;
            color: {COLOR_TEXT};
            line-height: 1.1;
        }}
        .metric-delta {{
            margin-top: 0.4rem;
            font-size: 0.92rem;
            color: {COLOR_MUTED};
        }}
        .section-note {{
            color: {COLOR_MUTED};
            font-size: 0.9rem;
        }}
        div[data-testid="stMetric"] {{
            background: {COLOR_CARD};
            border: 1px solid #d9e2ec;
            padding: 0.8rem 1rem;
            border-radius: 16px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner=False)
def get_bq_client() -> bigquery.Client:
    keyfile = Path(os.getenv("GOOGLE_APPLICATION_CREDENTIALS", str(DEFAULT_KEYFILE)))
    credentials = service_account.Credentials.from_service_account_file(keyfile)
    return bigquery.Client(project=PROJECT_ID, credentials=credentials)


@st.cache_data(ttl=1800, show_spinner=False)
def run_query(query: str) -> pd.DataFrame:
    client = get_bq_client()
    return client.query(query).to_dataframe()


def local_table_path(table: str) -> Path:
    return LOCAL_DATA_DIR / f"{table}.parquet"


def load_local_table(table: str) -> pd.DataFrame | None:
    path = local_table_path(table)
    if not path.exists():
        return None
    return pd.read_parquet(path)


def load_table(dataset: str, table: str) -> pd.DataFrame:
    query = f"select * from `{PROJECT_ID}.{dataset}.{table}`"
    return run_query(query)


def try_load_table(dataset: str, table: str, allow_bigquery: bool = True) -> pd.DataFrame | None:
    local_frame = load_local_table(table)
    if local_frame is not None:
        return local_frame
    if not allow_bigquery:
        return None
    try:
        return load_table(dataset, table)
    except NotFound:
        return None


def enrich_time_columns(frame: pd.DataFrame | None) -> pd.DataFrame | None:
    if frame is None:
        return None

    enriched = frame.copy()
    if "data_referencia" in enriched.columns:
        enriched["data_referencia"] = pd.to_datetime(enriched["data_referencia"])
        if "ano" not in enriched.columns:
            enriched["ano"] = enriched["data_referencia"].dt.year
        if "ano_mes" not in enriched.columns:
            enriched["ano_mes"] = enriched["data_referencia"].dt.strftime("%Y-%m")

    if "ano_mes" in enriched.columns:
        enriched["ano_mes"] = enriched["ano_mes"].astype(str)

    return enriched


def has_columns(frame: pd.DataFrame, columns: list[str]) -> bool:
    return set(columns).issubset(frame.columns)


@st.cache_data(ttl=1800, show_spinner=False)
def load_data() -> dict[str, pd.DataFrame | None]:
    allow_bigquery = not LOCAL_DATA_DIR.exists()
    tables: dict[str, pd.DataFrame | None] = {
        "performance": try_load_table("dbt_desafio_analista_marts", "mart_performance_tmae", allow_bigquery),
        "coelba": try_load_table("dbt_desafio_analista_marts", "mart_coelba_tmae", allow_bigquery),
        "ranking": try_load_table("dbt_desafio_analista_marts", "mart_ranking_distribuidoras", allow_bigquery),
        "componentes": try_load_table("dbt_desafio_analista_marts", "mart_componentes_tmae", allow_bigquery),
        "ml_features": try_load_table("dbt_desafio_analista_marts", "mart_ml_features_tmae", allow_bigquery),
        "ml_resultados": try_load_table("dbt_desafio_analista_marts", "ml_tmae_resultados", allow_bigquery),
        "dim_tempo": try_load_table("dbt_desafio_analista_dimensions", "dim_tempo", allow_bigquery),
        "dim_distribuidora": try_load_table("dbt_desafio_analista_dimensions", "dim_distribuidora", allow_bigquery),
    }

    for name, frame in tables.items():
        tables[name] = enrich_time_columns(frame)
    return tables


def detect_data_source(data: dict[str, pd.DataFrame | None]) -> str:
    local_main = local_table_path("mart_performance_tmae")
    if local_main.exists():
        return "Arquivos locais Parquet"
    if data.get("performance") is not None:
        return "BigQuery"
    return "Indisponivel"


def format_number(value: float | int | None, suffix: str = "", digits: int = 2) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{value:,.{digits}f}{suffix}".replace(",", "X").replace(".", ",").replace("X", ".")


def metric_card(label: str, value: str, delta: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_filters(performance: pd.DataFrame) -> dict[str, list[str]]:
    st.sidebar.header("Filtros")
    anos = sorted(performance["ano"].dropna().astype(int).unique().tolist())
    anos_default = anos[-5:] if len(anos) > 5 else anos
    anos_sel = st.sidebar.multiselect("Ano", anos, default=anos_default)

    ano_mes_options = sorted(performance["ano_mes"].dropna().unique().tolist())
    ano_mes_sel = st.sidebar.multiselect("Ano-Mes", ano_mes_options, default=ano_mes_options)

    regioes = sorted(performance["regiao"].dropna().unique().tolist())
    regiao_sel = st.sidebar.multiselect("Regiao", regioes, default=regioes)

    grupos = sorted(performance["grupo_economico"].dropna().unique().tolist())
    grupo_sel = st.sidebar.multiselect("Grupo Economico", grupos, default=grupos)

    distribuidoras = sorted(performance["distribuidora"].dropna().unique().tolist())
    distrib_default = ["Neoenergia Coelba"] if "Neoenergia Coelba" in distribuidoras else distribuidoras
    distrib_sel = st.sidebar.multiselect("Distribuidora", distribuidoras, default=distrib_default)

    return {
        "anos": anos_sel,
        "ano_mes": ano_mes_sel,
        "regiao": regiao_sel,
        "grupo": grupo_sel,
        "distribuidora": distrib_sel,
    }


def apply_common_filters(frame: pd.DataFrame, filters: dict[str, list[str]]) -> pd.DataFrame:
    filtered = frame.copy()
    if "ano" in filtered.columns and filters["anos"]:
        filtered = filtered[filtered["ano"].isin(filters["anos"])]
    if "ano_mes" in filtered.columns and filters["ano_mes"]:
        filtered = filtered[filtered["ano_mes"].isin(filters["ano_mes"])]
    if "regiao" in filtered.columns and filters["regiao"]:
        filtered = filtered[filtered["regiao"].isin(filters["regiao"])]
    if "grupo_economico" in filtered.columns and filters["grupo"]:
        filtered = filtered[filtered["grupo_economico"].isin(filters["grupo"])]
    if "distribuidora" in filtered.columns and filters["distribuidora"]:
        filtered = filtered[filtered["distribuidora"].isin(filters["distribuidora"])]
    return filtered


def apply_coelba_filters(frame: pd.DataFrame, filters: dict[str, list[str]]) -> pd.DataFrame:
    filtered = frame.copy()
    if "ano" in filtered.columns and filters["anos"]:
        filtered = filtered[filtered["ano"].isin(filters["anos"])]
    if "ano_mes" in filtered.columns and filters["ano_mes"]:
        filtered = filtered[filtered["ano_mes"].isin(filters["ano_mes"])]
    return filtered


def line_chart(frame: pd.DataFrame, x: str, y: list[str], title: str) -> go.Figure:
    fig = go.Figure()
    palette = [COLOR_PRIMARY, COLOR_GREEN, COLOR_BLUE_SOFT]
    for idx, column in enumerate(y):
        if column not in frame.columns:
            continue
        fig.add_trace(
            go.Scatter(
                x=frame[x],
                y=frame[column],
                mode="lines+markers",
                name=column.replace("_", " ").title(),
                line={"width": 3, "color": palette[idx % len(palette)]},
            )
        )
    fig.update_layout(
        title=title,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin={"l": 10, "r": 10, "t": 50, "b": 10},
        legend={"orientation": "h", "y": 1.1},
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#E6EEF5")
    return fig


def section_header(title: str, note: str) -> None:
    st.subheader(title)
    st.markdown(f"<div class='section-note'>{note}</div>", unsafe_allow_html=True)


def page_resumo(coelba: pd.DataFrame) -> None:
    section_header(
        "Resumo Executivo",
        "Leitura rapida da performance da Neoenergia Coelba contra a media nacional.",
    )
    latest = coelba.sort_values("data_referencia").dropna(subset=["data_referencia"]).iloc[-1]
    cols = st.columns(5)
    with cols[0]:
        metric_card("TMAE Coelba", format_number(latest["tmae"]))
    with cols[1]:
        metric_card("TMAE Brasil", format_number(latest["media_tmae_brasil"]))
    with cols[2]:
        delta = latest["tmae"] - latest["media_tmae_brasil"]
        metric_card(
            "Dif. vs Brasil",
            format_number(delta),
            "Melhor" if delta < 0 else "Pior" if delta > 0 else "Igual",
        )
    with cols[3]:
        metric_card("Ranking Nacional", format_number(latest["ranking_nacional"], digits=0))
    with cols[4]:
        metric_card("Status", str(latest["classificacao_performance"]))

    left, right = st.columns((1.9, 1.1))
    with left:
        fig = line_chart(
            coelba.sort_values("data_referencia"),
            "ano_mes",
            ["tmae", "media_tmae_brasil"],
            "Coelba vs Brasil ao longo do tempo",
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        varia = px.bar(
            coelba.sort_values("data_referencia"),
            x="ano_mes",
            y="variacao_abs_mes_anterior",
            color="variacao_abs_mes_anterior",
            color_continuous_scale=[[0, COLOR_GREEN], [0.5, COLOR_WARNING], [1, COLOR_DANGER]],
            title="Variacao mensal do TMAE",
        )
        varia.update_layout(paper_bgcolor="white", plot_bgcolor="white", coloraxis_showscale=False)
        st.plotly_chart(varia, use_container_width=True)

    st.dataframe(
        coelba[
            ["ano_mes", "tmae", "ranking_nacional", "diferenca_vs_brasil", "tendencia"]
        ].sort_values("ano_mes", ascending=False),
        use_container_width=True,
        hide_index=True,
    )


def page_ranking(ranking: pd.DataFrame) -> None:
    section_header(
        "Ranking Nacional",
        "Comparacao entre distribuidoras com TMAE crescente: menor tempo recebe o melhor ranking.",
    )
    latest_period = ranking["data_referencia"].max()
    current = ranking[ranking["data_referencia"] == latest_period].copy()
    current = current.sort_values("tmae").head(15)

    top = st.columns(4)
    coelba = ranking[ranking["distribuidora"] == "Neoenergia Coelba"].sort_values("data_referencia")
    latest_coelba = coelba.iloc[-1] if not coelba.empty else None
    with top[0]:
        metric_card(
            "Ranking Coelba",
            format_number(latest_coelba["ranking_nacional"], digits=0) if latest_coelba is not None else "-",
        )
    with top[1]:
        metric_card("Benchmark", str(current.iloc[0]["distribuidora"]) if not current.empty else "-")
    with top[2]:
        metric_card("Melhor TMAE", format_number(current.iloc[0]["tmae"]) if not current.empty else "-")
    with top[3]:
        metric_card("Pior TMAE", format_number(current.iloc[-1]["tmae"]) if not current.empty else "-")

    fig = px.bar(
        current,
        x="tmae",
        y="distribuidora",
        orientation="h",
        color="distribuidora",
        title="Top 15 distribuidoras no ultimo periodo filtrado",
        color_discrete_sequence=[COLOR_PRIMARY] * len(current),
    )
    fig.update_layout(showlegend=False, paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        ranking[
            [
                "data_referencia",
                "distribuidora",
                "tmae",
                "ranking_nacional",
                "ranking_regional",
                "ranking_grupo",
                "diferenca_vs_brasil",
            ]
        ].sort_values(["data_referencia", "ranking_nacional"], ascending=[False, True]),
        use_container_width=True,
        hide_index=True,
    )


def page_evolucao(performance: pd.DataFrame) -> None:
    section_header(
        "Evolucao Temporal",
        "Serie historica consolidada da Coelba com media movel e leitura de melhora ou piora.",
    )
    coelba = performance[performance["flag_neoenergia_coelba"]].sort_values("data_referencia")

    left, right = st.columns((1.9, 1.1))
    with left:
        fig = line_chart(coelba, "ano_mes", ["tmae", "media_movel_3m", "media_tmae_brasil"], "Evolucao do TMAE")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        tendencia = coelba["tendencia"].value_counts().reset_index()
        tendencia.columns = ["tendencia", "quantidade"]
        pie = px.pie(
            tendencia,
            values="quantidade",
            names="tendencia",
            title="Distribuicao da tendencia",
            color="tendencia",
            color_discrete_map={
                "Melhora": COLOR_GREEN,
                "Piora": COLOR_DANGER,
                "Estavel": COLOR_WARNING,
                "Sem historico": COLOR_BLUE_SOFT,
            },
        )
        pie.update_layout(paper_bgcolor="white")
        st.plotly_chart(pie, use_container_width=True)

    st.dataframe(
        coelba[
            ["ano_mes", "tmae", "tmae_mes_anterior", "variacao_abs_mes_anterior", "variacao_pct_mes_anterior", "tendencia"]
        ].sort_values("ano_mes", ascending=False),
        use_container_width=True,
        hide_index=True,
    )


def page_componentes(componentes: pd.DataFrame) -> None:
    section_header(
        "Componentes do TMAE",
        "Analise de Preparacao, Deslocamento e Execucao para entender o principal gargalo operacional.",
    )
    required = [
        "data_referencia",
        "tmp",
        "tmd",
        "tme",
        "participacao_tmp",
        "participacao_tmd",
        "participacao_tme",
        "principal_componente_tmae",
    ]
    if not has_columns(componentes, required):
        missing = sorted(set(required) - set(componentes.columns))
        st.error(f"A mart de componentes nao possui todas as colunas esperadas. Faltando: {', '.join(missing)}.")
        return

    latest = componentes.sort_values("data_referencia").dropna(subset=["data_referencia"]).iloc[-1]
    top = st.columns(4)
    with top[0]:
        metric_card("TMP Medio", format_number(latest["tmp"]))
    with top[1]:
        metric_card("TMD Medio", format_number(latest["tmd"]))
    with top[2]:
        metric_card("TME Medio", format_number(latest["tme"]))
    with top[3]:
        metric_card("Principal Componente", str(latest["principal_componente_tmae"]))

    left, right = st.columns(2)
    with left:
        comp = componentes.sort_values("data_referencia").copy()
        comp_long = comp.melt(
            id_vars=["ano_mes"],
            value_vars=["participacao_tmp", "participacao_tmd", "participacao_tme"],
            var_name="componente",
            value_name="participacao",
        )
        fig = px.bar(
            comp_long,
            x="ano_mes",
            y="participacao",
            color="componente",
            title="Participacao dos componentes no TMAE",
            color_discrete_map={
                "participacao_tmp": COLOR_PRIMARY,
                "participacao_tmd": COLOR_GREEN,
                "participacao_tme": COLOR_BLUE_SOFT,
            },
        )
        fig.update_layout(barmode="stack", paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        coelba_componentes = componentes[componentes["flag_neoenergia_coelba"]].sort_values("data_referencia")
        if coelba_componentes.empty:
            referencia = componentes.sort_values("data_referencia").iloc[-1]
            compare_title = f"{referencia['distribuidora']} vs Brasil por componente"
            latest_compare = referencia
            serie_local = str(referencia["distribuidora"])
        else:
            compare_title = "Coelba vs Brasil por componente"
            latest_compare = coelba_componentes.iloc[-1]
            serie_local = "Coelba"

        compare = pd.DataFrame(
            {
                "componente": ["TMP", "TMD", "TME"],
                serie_local: [latest_compare["tmp"], latest_compare["tmd"], latest_compare["tme"]],
                "Brasil": [latest_compare["tmp_brasil"], latest_compare["tmd_brasil"], latest_compare["tme_brasil"]],
            }
        ).melt(id_vars="componente", var_name="serie", value_name="valor")
        fig = px.bar(
            compare,
            x="componente",
            y="valor",
            color="serie",
            barmode="group",
            title=compare_title,
            color_discrete_map={serie_local: COLOR_PRIMARY, "Brasil": COLOR_GREEN},
        )
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        componentes[
            ["data_referencia", "distribuidora", "principal_componente_tmae", "diferenca_tmae_calculado", "flag_tmae_inconsistente"]
        ].sort_values(["data_referencia", "distribuidora"], ascending=[False, True]),
        use_container_width=True,
        hide_index=True,
    )


def page_ml(ml_features: pd.DataFrame, ml_resultados: pd.DataFrame | None) -> None:
    section_header(
        "Inteligencia Analitica",
        "Camada complementar de anomalias, clusters e previsao. Requer a tabela ml_tmae_resultados no BigQuery.",
    )
    if ml_resultados is None:
        st.warning(
            "A tabela ml_tmae_resultados ainda nao existe no BigQuery. Execute `python scripts/train_ml_model.py` para liberar esta aba."
        )
        return

    required = [
        "distribuidora",
        "data_referencia",
        "tmae",
        "tmae_previsto",
        "score_anomalia",
        "flag_anomalia",
        "interpretacao_cluster",
        "tendencia_prevista",
        "recomendacao_negocio",
    ]
    if not has_columns(ml_resultados, required):
        missing = sorted(set(required) - set(ml_resultados.columns))
        st.error(f"A tabela ml_tmae_resultados nao possui todas as colunas esperadas. Faltando: {', '.join(missing)}.")
        return

    if "data_referencia" in ml_resultados.columns:
        ml_resultados = ml_resultados.sort_values("data_referencia")

    top = st.columns(4)
    anomalies = int(ml_resultados["flag_anomalia"].fillna(False).sum())
    total = len(ml_resultados)
    coelba_ml = ml_resultados[ml_resultados["distribuidora"] == "Neoenergia Coelba"]
    latest_coelba = coelba_ml.iloc[-1] if not coelba_ml.empty else None

    with top[0]:
        metric_card("Anomalias", format_number(anomalies, digits=0))
    with top[1]:
        metric_card("Pct. de Anomalia", format_number((anomalies / total * 100) if total else 0, suffix="%"))
    with top[2]:
        metric_card("Cluster Coelba", str(latest_coelba["interpretacao_cluster"]) if latest_coelba is not None else "-")
    with top[3]:
        metric_card("Tendencia Prevista", str(latest_coelba["tendencia_prevista"]) if latest_coelba is not None else "-")

    left, right = st.columns(2)
    with left:
        scatter = px.scatter(
            ml_resultados,
            x="tmae",
            y="score_anomalia",
            color="interpretacao_cluster",
            hover_data=["distribuidora", "data_referencia"],
            title="Clusters e score de anomalia",
        )
        scatter.update_layout(paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(scatter, use_container_width=True)
    with right:
        if not coelba_ml.empty:
            line = go.Figure()
            line.add_trace(go.Scatter(x=coelba_ml["data_referencia"], y=coelba_ml["tmae"], mode="lines+markers", name="TMAE"))
            line.add_trace(
                go.Scatter(
                    x=coelba_ml["data_referencia"],
                    y=coelba_ml["tmae_previsto"],
                    mode="lines+markers",
                    name="TMAE Previsto",
                )
            )
            line.update_layout(
                title="Coelba: realizado vs previsto",
                paper_bgcolor="white",
                plot_bgcolor="white",
                margin={"l": 10, "r": 10, "t": 50, "b": 10},
            )
            st.plotly_chart(line, use_container_width=True)

    st.dataframe(
        ml_resultados[
            [
                "distribuidora",
                "data_referencia",
                "score_anomalia",
                "flag_anomalia",
                "interpretacao_cluster",
                "recomendacao_negocio",
            ]
        ].sort_values(["data_referencia", "score_anomalia"], ascending=[False, False]),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    inject_css()
    st.markdown(
        """
        <div class="hero">
            <h1>Neoenergia Coelba | Dashboard TMAE</h1>
            <p>Camada executiva em Streamlit sobre as marts analiticas do BigQuery. Menor TMAE significa melhor desempenho operacional.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("Carregando dados analiticos..."):
        data = load_data()

    source_label = detect_data_source(data)
    if source_label == "Arquivos locais Parquet":
        st.info("Fonte de dados ativa: arquivos locais Parquet em `data/offline/`.")
    elif source_label == "BigQuery":
        st.info("Fonte de dados ativa: BigQuery.")

    performance = data["performance"]
    if performance is None or performance.empty:
        st.error("Nao foi possivel carregar a mart principal nem por arquivos locais nem por BigQuery.")
        return

    filters = build_filters(performance)
    performance_filtered = apply_common_filters(performance, filters)
    coelba_filtered = apply_coelba_filters(data["coelba"], filters)
    ranking_filtered = apply_common_filters(data["ranking"], filters)
    componentes_filtered = apply_common_filters(data["componentes"], filters)
    ml_features_filtered = apply_common_filters(data["ml_features"], filters)

    ml_resultados = data["ml_resultados"]
    if ml_resultados is not None:
        ml_resultados = ml_resultados.copy()
        if "data_referencia" in ml_resultados.columns:
            ml_resultados["ano_mes"] = ml_resultados["data_referencia"].dt.strftime("%Y-%m")
        ml_resultados = apply_common_filters(ml_resultados, filters)

    if performance_filtered.empty:
        st.warning("Os filtros selecionados nao retornaram dados.")
        return

    tab_resumo, tab_ranking, tab_evolucao, tab_componentes, tab_ml = st.tabs(
        [
            "Resumo Executivo",
            "Ranking Nacional",
            "Evolucao Temporal",
            "Componentes TMAE",
            "Inteligencia Analitica",
        ]
    )

    with tab_resumo:
        page_resumo(coelba_filtered if not coelba_filtered.empty else data["coelba"])
    with tab_ranking:
        page_ranking(ranking_filtered if not ranking_filtered.empty else data["ranking"])
    with tab_evolucao:
        page_evolucao(performance_filtered)
    with tab_componentes:
        page_componentes(componentes_filtered if not componentes_filtered.empty else data["componentes"])
    with tab_ml:
        page_ml(ml_features_filtered, ml_resultados)


if __name__ == "__main__":
    main()
