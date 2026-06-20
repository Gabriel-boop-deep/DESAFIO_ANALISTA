from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pyarrow.parquet as pq
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
LOCAL_DATA_DIR = PROJECT_ROOT / "data" / "offline"
LOGO_PATH = PROJECT_ROOT / "FIGMA" / "nova-marca-neoenergia-coelba.png"
COLOR_BG = "#031E16"
COLOR_PANEL = "#073526"
COLOR_PANEL_SOFT = "#0A4732"
COLOR_BORDER = "#1A7F5A"
COLOR_TEXT = "#F5F7FA"
COLOR_MUTED = "#B8C4CC"
COLOR_GREEN = "#00D46A"
COLOR_GREEN_SOFT = "#77F38B"
COLOR_BLUE = "#1FA7FF"
COLOR_ORANGE = "#F28C28"
COLOR_RED = "#D94F4F"
COLOR_PURPLE = "#8B5CF6"


st.set_page_config(
    page_title="Neoenergia Coelba | Laboratório Complementar",
    page_icon="dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                radial-gradient(circle at top right, rgba(0, 212, 106, 0.25), transparent 24%),
                linear-gradient(180deg, #02160f 0%, {COLOR_BG} 100%);
            color: {COLOR_TEXT};
        }}
        [data-testid="stHeader"] {{
            background: transparent;
            height: 0;
        }}
        [data-testid="stHeader"] * {{
            display: none;
        }}
        [data-testid="stToolbar"] {{
            visibility: hidden;
            height: 0;
            position: fixed;
        }}
        #MainMenu {{
            visibility: hidden;
        }}
        .block-container {{
            padding-top: 0.2rem;
            padding-bottom: 1.5rem;
        }}
        .hero {{
            background:
                linear-gradient(135deg, rgba(0, 70, 43, 0.96) 0%, rgba(3, 30, 22, 0.98) 62%),
                radial-gradient(circle at top right, rgba(0, 212, 106, 0.15), transparent 30%);
            border: 1px solid rgba(119, 243, 139, 0.28);
            border-radius: 28px;
            padding: 1.5rem 1.7rem;
            color: {COLOR_TEXT};
            box-shadow: 0 22px 40px rgba(0, 0, 0, 0.28);
            margin-bottom: 1rem;
        }}
        .hero h1 {{
            margin: 0;
            font-size: 2.25rem;
            font-weight: 800;
            letter-spacing: -0.03em;
        }}
        .hero p {{
            margin: 0.45rem 0 0 0;
            color: {COLOR_MUTED};
            font-size: 1rem;
        }}
        .pill {{
            display: inline-block;
            padding: 0.45rem 0.8rem;
            border: 1px solid rgba(119, 243, 139, 0.35);
            border-radius: 999px;
            font-size: 0.86rem;
            margin-right: 0.5rem;
            margin-top: 0.7rem;
            background: rgba(119, 243, 139, 0.08);
        }}
        .metric-card {{
            background: linear-gradient(180deg, rgba(7, 53, 38, 0.98) 0%, rgba(4, 38, 27, 0.98) 100%);
            border: 1px solid rgba(26, 127, 90, 0.7);
            border-radius: 22px;
            padding: 1rem 1.1rem;
            min-height: 126px;
            box-shadow: 0 18px 34px rgba(0, 0, 0, 0.22);
        }}
        .metric-label {{
            color: {COLOR_MUTED};
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .metric-value {{
            color: {COLOR_TEXT};
            font-size: 1.9rem;
            font-weight: 800;
            margin-top: 0.35rem;
            line-height: 1.05;
        }}
        .metric-delta {{
            color: {COLOR_MUTED};
            margin-top: 0.4rem;
            font-size: 0.92rem;
        }}
        .section-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: {COLOR_TEXT};
            margin-bottom: 0.2rem;
        }}
        .section-note {{
            color: {COLOR_MUTED};
            font-size: 0.92rem;
            margin-bottom: 0.85rem;
        }}
        div[data-testid="stDataFrame"] {{
            border: 1px solid rgba(26, 127, 90, 0.6);
            border-radius: 18px;
            overflow: hidden;
        }}
        div[data-testid="stMetric"] {{
            background: rgba(7, 53, 38, 0.98);
            border: 1px solid rgba(26, 127, 90, 0.7);
            border-radius: 18px;
            padding: 0.8rem 1rem;
        }}
        div[data-baseweb="tab-list"] {{
            gap: 0.25rem;
        }}
        div[data-baseweb="tab"] {{
            background: rgba(7, 53, 38, 0.75);
            border-radius: 14px 14px 0 0;
            color: {COLOR_MUTED};
            border: 1px solid rgba(26, 127, 90, 0.4);
            padding: 0.75rem 1rem;
        }}
        div[data-baseweb="tab"][aria-selected="true"] {{
            color: {COLOR_TEXT};
            border-bottom-color: transparent;
            background: rgba(10, 71, 50, 0.95);
        }}
        .catalog-card {{
            background: rgba(7, 53, 38, 0.88);
            border: 1px solid rgba(26, 127, 90, 0.65);
            border-radius: 18px;
            padding: 1rem 1rem 0.95rem 1rem;
            min-height: 172px;
        }}
        .catalog-layer {{
            color: {COLOR_GREEN_SOFT};
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .catalog-model {{
            color: {COLOR_TEXT};
            font-size: 1.08rem;
            font-weight: 800;
            margin-top: 0.25rem;
        }}
        .catalog-desc {{
            color: {COLOR_MUTED};
            font-size: 0.9rem;
            margin-top: 0.45rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


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


def section_header(title: str, note: str) -> None:
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-note'>{note}</div>", unsafe_allow_html=True)


def format_number(value: float | int | None, digits: int = 2, suffix: str = "") -> str:
    if value is None or pd.isna(value):
        return "-"
    formatted = f"{value:,.{digits}f}{suffix}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def format_percent(value: float | None, digits: int = 1) -> str:
    if value is None or pd.isna(value):
        return "-"
    formatted = f"{value * 100:,.{digits}f}%"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def local_table_path(table_name: str) -> Path:
    return LOCAL_DATA_DIR / f"{table_name}.parquet"


def read_parquet(table_name: str) -> pd.DataFrame:
    path = local_table_path(table_name)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo local ausente: {path}")
    table = pq.read_table(path)
    return table.to_pandas(ignore_metadata=True)


def enrich_frame(frame: pd.DataFrame) -> pd.DataFrame:
    enriched = frame.copy()
    if "data_referencia" in enriched.columns:
        enriched["data_referencia"] = pd.to_datetime(enriched["data_referencia"])
    if "ano_mes" in enriched.columns:
        enriched["ano_mes"] = enriched["ano_mes"].astype(str)
    elif "data_referencia" in enriched.columns:
        enriched["ano_mes"] = enriched["data_referencia"].dt.strftime("%Y-%m")
    if "ano" not in enriched.columns and "data_referencia" in enriched.columns:
        enriched["ano"] = enriched["data_referencia"].dt.year
    return enriched


def derive_performance_features(frame: pd.DataFrame) -> pd.DataFrame:
    enriched = frame.copy()

    if "quantidade_distribuidoras_brasil" not in enriched.columns:
        enriched["quantidade_distribuidoras_brasil"] = (
            enriched.groupby("data_referencia")["distribuidora"].transform("nunique")
        )

    if "quartil_performance" not in enriched.columns and {"data_referencia", "tmae"}.issubset(enriched.columns):
        pct_rank = enriched.groupby("data_referencia")["tmae"].rank(method="average", pct=True)
        enriched["quartil_performance"] = pd.cut(
            pct_rank,
            bins=[0.0, 0.25, 0.50, 0.75, 1.0],
            labels=[1, 2, 3, 4],
            include_lowest=True,
        ).astype("Int64")

    if "menor_tmae_brasil" not in enriched.columns:
        enriched["menor_tmae_brasil"] = enriched.groupby("data_referencia")["tmae"].transform("min")

    if "maior_tmae_brasil" not in enriched.columns:
        enriched["maior_tmae_brasil"] = enriched.groupby("data_referencia")["tmae"].transform("max")

    if "score_performance" not in enriched.columns:
        denominator = (enriched["maior_tmae_brasil"] - enriched["menor_tmae_brasil"]).replace(0, np.nan)
        enriched["score_performance"] = 100 * (
            (enriched["maior_tmae_brasil"] - enriched["tmae"]) / denominator
        )
        enriched["score_performance"] = enriched["score_performance"].fillna(100.0)

    if "tmae_benchmark_nacional" not in enriched.columns:
        enriched["tmae_benchmark_nacional"] = enriched.groupby("data_referencia")["tmae"].transform("min")

    if "tmae_limite_top_10" not in enriched.columns:
        def _top10_limit(series: pd.Series) -> float:
            ordered = series.sort_values().reset_index(drop=True)
            idx = min(9, len(ordered) - 1)
            return float(ordered.iloc[idx])

        limit_map = enriched.groupby("data_referencia")["tmae"].apply(_top10_limit)
        enriched["tmae_limite_top_10"] = enriched["data_referencia"].map(limit_map)

    if "distancia_para_benchmark" not in enriched.columns:
        enriched["distancia_para_benchmark"] = enriched["tmae"] - enriched["tmae_benchmark_nacional"]

    if "distancia_para_top_10" not in enriched.columns:
        enriched["distancia_para_top_10"] = enriched["tmae"] - enriched["tmae_limite_top_10"]

    if "tmae_ano_anterior" not in enriched.columns:
        enriched = enriched.sort_values(["distribuidora", "data_referencia"]).copy()
        enriched["tmae_ano_anterior"] = enriched.groupby("distribuidora")["tmae"].shift(12)

    if "flag_outlier_tmae" not in enriched.columns:
        def _zscore(series: pd.Series) -> pd.Series:
            std = series.std(ddof=0)
            if pd.isna(std) or std == 0:
                return pd.Series(np.nan, index=series.index)
            return (series - series.mean()) / std

        zscore = enriched.groupby("data_referencia")["tmae"].transform(_zscore)
        enriched["zscore_tmae_brasil"] = zscore if "zscore_tmae_brasil" not in enriched.columns else enriched["zscore_tmae_brasil"]
        enriched["flag_outlier_tmae"] = zscore.abs().fillna(0) >= 2

    if "tendencia_anual" not in enriched.columns:
        enriched["tendencia_anual"] = np.where(
            enriched.get("tmae_ano_anterior").notna() if "tmae_ano_anterior" in enriched.columns else False,
            np.where(
                (enriched["tmae"] - enriched["tmae_ano_anterior"]) < 0,
                "Melhora anual",
                np.where(
                    (enriched["tmae"] - enriched["tmae_ano_anterior"]) > 0,
                    "Piora anual",
                    "Estavel anual",
                ),
            ),
            "Sem base anual",
        )

    return enriched


@st.cache_data(show_spinner=False)
def load_data() -> dict[str, pd.DataFrame]:
    tables = {
        "performance": derive_performance_features(enrich_frame(read_parquet("mart_performance_tmae"))),
        "coelba": derive_performance_features(enrich_frame(read_parquet("mart_coelba_tmae"))),
        "ranking": enrich_frame(read_parquet("mart_ranking_distribuidoras")),
        "componentes": enrich_frame(read_parquet("mart_componentes_tmae")),
        "ml_features": enrich_frame(read_parquet("mart_ml_features_tmae")),
        "ml_resultados": enrich_frame(read_parquet("ml_tmae_resultados")),
        "dim_tempo": enrich_frame(read_parquet("dim_tempo")),
        "dim_distribuidora": enrich_frame(read_parquet("dim_distribuidora")),
    }
    return tables


def build_filters(data: dict[str, pd.DataFrame]) -> dict[str, list[str] | list[int]]:
    performance = data["performance"]
    dim_tempo = data["dim_tempo"]
    dim_distribuidora = data["dim_distribuidora"]

    st.sidebar.header("Filtros")
    st.sidebar.caption("A aplicação usa arquivos Parquet exportados e prontos para consumo.")

    anos = sorted(dim_tempo["ano"].dropna().astype(int).unique().tolist())
    anos_default = anos[-5:] if len(anos) > 5 else anos
    anos_sel = st.sidebar.multiselect("Ano", anos, default=anos_default)

    ano_mes_options = sorted(dim_tempo["ano_mes"].dropna().astype(str).unique().tolist())
    ano_mes_default = ano_mes_options[-18:] if len(ano_mes_options) > 18 else ano_mes_options
    ano_mes_sel = st.sidebar.multiselect("Ano-Mes", ano_mes_options, default=ano_mes_default)

    regioes = sorted(dim_distribuidora["regiao"].dropna().astype(str).unique().tolist())
    regiao_sel = st.sidebar.multiselect("Regiao", regioes, default=regioes)

    grupos = sorted(dim_distribuidora["grupo_economico"].dropna().astype(str).unique().tolist())
    grupo_sel = st.sidebar.multiselect("Grupo Economico", grupos, default=grupos)

    distribuidoras = sorted(dim_distribuidora["distribuidora"].dropna().astype(str).unique().tolist())
    default_distrib = ["Neoenergia Coelba"] if "Neoenergia Coelba" in distribuidoras else distribuidoras[:1]
    distrib_sel = st.sidebar.multiselect("Distribuidora", distribuidoras, default=default_distrib)

    st.sidebar.divider()
    st.sidebar.metric("Linhas locais", format_number(len(performance), digits=0))
    st.sidebar.metric(
        "Cobertura temporal",
        f"{performance['data_referencia'].min():%Y-%m} a {performance['data_referencia'].max():%Y-%m}",
    )

    return {
        "anos": anos_sel,
        "ano_mes": ano_mes_sel,
        "regiao": regiao_sel,
        "grupo": grupo_sel,
        "distribuidora": distrib_sel,
    }


def apply_filters(frame: pd.DataFrame, filters: dict[str, list[str] | list[int]]) -> pd.DataFrame:
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


def plot_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor=COLOR_PANEL,
        plot_bgcolor=COLOR_PANEL,
        font={"color": COLOR_TEXT},
        margin={"l": 18, "r": 18, "t": 54, "b": 18},
        legend={"orientation": "h", "y": 1.06, "x": 0},
    )
    fig.update_xaxes(showgrid=False, zeroline=False, color=COLOR_MUTED)
    fig.update_yaxes(gridcolor="rgba(184, 196, 204, 0.18)", zeroline=False, color=COLOR_MUTED)
    return fig


def hero(data: dict[str, pd.DataFrame]) -> None:
    performance = data["performance"]
    coelba = data["coelba"]
    latest_coelba = coelba.sort_values("data_referencia").iloc[-1]
    min_dt = performance["data_referencia"].min().strftime("%Y-%m")
    max_dt = performance["data_referencia"].max().strftime("%Y-%m")
    logo_col, hero_col = st.columns((0.24, 1.0), gap="medium")
    with logo_col:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), use_container_width=True)
        else:
            st.markdown(
                """
                <div class="hero">
                    <p style="margin:0; text-align:center;">Logo institucional não encontrada.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    with hero_col:
        st.markdown(
            f"""
            <div class="hero">
                <h1>Laboratório Complementar TMAE</h1>
                <p>
                    Aplicação complementar ao Power BI, desenhada para ampliar a leitura com visões de risco,
                    previsão, segmentação e observabilidade da modelagem analítica.
                </p>
                <span class="pill">Marca: Neoenergia Coelba</span>
                <span class="pill">Base: data/offline</span>
                <span class="pill">Cobertura: {min_dt} a {max_dt}</span>
                <span class="pill">Último TMAE Coelba: {format_number(latest_coelba['tmae'])}</span>
                <span class="pill">Regra: menor TMAE = melhor desempenho</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def overview_tab(data: dict[str, pd.DataFrame], filters: dict[str, list[str] | list[int]]) -> None:
    performance = apply_filters(data["performance"], filters)
    if performance.empty:
        st.warning("Sem dados para os filtros selecionados.")
        return

    coelba = performance[performance["flag_neoenergia_coelba"]]
    latest_coelba = coelba.sort_values("data_referencia").iloc[-1]
    volatility = float(coelba["tmae"].std()) if len(coelba) > 1 else np.nan
    outlier_share = float(coelba["flag_outlier_tmae"].mean()) if "flag_outlier_tmae" in coelba.columns else np.nan

    cols = st.columns(5)
    with cols[0]:
        metric_card("Score da Coelba", format_number(latest_coelba["score_performance"], digits=1))
    with cols[1]:
        metric_card("Gap para benchmark", format_number(latest_coelba["distancia_para_benchmark"], digits=1))
    with cols[2]:
        metric_card("Gap para Top 10", format_number(latest_coelba["distancia_para_top_10"], digits=1))
    with cols[3]:
        metric_card("Volatilidade", format_number(volatility, digits=1), "Desvio padrão do TMAE")
    with cols[4]:
        metric_card("Meses outlier", format_percent(outlier_share, digits=1), "Participacao de alertas")

    left, right = st.columns((1.3, 1.0))
    with left:
        section_header(
            "Recuperação da Coelba vs Brasil",
            "Visão complementar para enxergar se a melhora recente está reduzindo o gap competitivo.",
        )
        trend_frame = coelba.sort_values("data_referencia")[
            [
                "data_referencia",
                "tmae",
                "media_tmae_brasil",
                "media_movel_3m",
                "distancia_para_benchmark",
            ]
        ]
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=trend_frame["data_referencia"],
                y=trend_frame["tmae"],
                mode="lines+markers",
                name="Coelba",
                line={"color": COLOR_GREEN, "width": 3},
            )
        )
        fig.add_trace(
            go.Scatter(
                x=trend_frame["data_referencia"],
                y=trend_frame["media_tmae_brasil"],
                mode="lines",
                name="Brasil",
                line={"color": COLOR_BLUE, "width": 2},
            )
        )
        fig.add_trace(
            go.Scatter(
                x=trend_frame["data_referencia"],
                y=trend_frame["media_movel_3m"],
                mode="lines",
                name="Média móvel Coelba",
                line={"color": COLOR_ORANGE, "width": 2, "dash": "dash"},
            )
        )
        fig.update_layout(title="Coelba vs Brasil vs média móvel")
        st.plotly_chart(plot_theme(fig), use_container_width=True)

    with right:
        section_header(
            "Mapa de tensão competitiva",
            "Distribuidoras posicionadas por score e distância para o benchmark para revelar bolsões de pressão.",
        )
        scatter = px.scatter(
            performance,
            x="score_performance",
            y="distancia_para_benchmark",
            color="regiao",
            hover_name="distribuidora",
            size="tmae",
            color_discrete_sequence=[COLOR_GREEN, COLOR_BLUE, COLOR_ORANGE, COLOR_PURPLE, COLOR_RED],
        )
        scatter.update_traces(marker={"line": {"width": 0}})
        scatter.update_layout(title="Score vs distância para benchmark")
        st.plotly_chart(plot_theme(scatter), use_container_width=True)

    section_header(
        "Diagnóstico executivo complementar",
        "Leitura consolidada para acompanhamento tático fora do Power BI.",
    )
    narrative = pd.DataFrame(
        [
            {
                "Pilar": "Posicionamento",
                "Leitura": f"Ranking atual da Coelba: {int(latest_coelba['ranking_nacional'])} de {int(latest_coelba['quantidade_distribuidoras_brasil'])}.",
            },
            {
                "Pilar": "Risco",
                "Leitura": f"Gap atual para o benchmark: {format_number(latest_coelba['distancia_para_benchmark'], digits=1)} minutos.",
            },
            {
                "Pilar": "Sinal de curto prazo",
                "Leitura": f"Tendência mensal: {latest_coelba['tendencia']}; tendência anual: {latest_coelba['tendencia_anual']}.",
            },
            {
                "Pilar": "Interpretacao",
                "Leitura": "A melhora recente existe, mas a distância para o benchmark ainda é alta e pede gestão dedicada.",
            },
        ]
    )
    st.dataframe(narrative, use_container_width=True, hide_index=True)


def forecasts_tab(data: dict[str, pd.DataFrame], filters: dict[str, list[str] | list[int]]) -> None:
    performance = apply_filters(data["performance"], filters)
    ml = apply_filters(data["ml_resultados"], filters)
    coelba_perf = performance[performance["flag_neoenergia_coelba"]].sort_values("data_referencia")
    coelba_ml = ml[ml["distribuidora"] == "Neoenergia Coelba"].sort_values("data_referencia")
    if coelba_perf.empty or coelba_ml.empty:
        st.warning("Sem dados de previsão para os filtros selecionados.")
        return

    latest_ml = coelba_ml.iloc[-1]
    anom_share = float(coelba_ml["flag_anomalia"].mean())
    mae = float((coelba_ml["erro_previsao"]).abs().mean())

    cols = st.columns(4)
    with cols[0]:
        metric_card("Cluster Coelba", str(latest_ml["cluster_performance"]))
    with cols[1]:
        metric_card("Tendência prevista", str(latest_ml["tendencia_prevista"]))
    with cols[2]:
        metric_card("Erro médio", format_number(mae, digits=1))
    with cols[3]:
        metric_card("Meses anômalos", format_percent(anom_share, digits=1))

    left, right = st.columns((1.2, 1.0))
    with left:
        section_header(
            "Previsto vs realizado",
            "Comparação entre o TMAE observado e a trilha prevista para a Coelba.",
        )
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=coelba_ml["data_referencia"],
                y=coelba_ml["tmae"],
                name="Realizado",
                mode="lines+markers",
                line={"color": COLOR_GREEN, "width": 3},
            )
        )
        fig.add_trace(
            go.Scatter(
                x=coelba_ml["data_referencia"],
                y=coelba_ml["tmae_previsto"],
                name="Previsto",
                mode="lines",
                line={"color": COLOR_BLUE, "width": 2, "dash": "dash"},
            )
        )
        fig.update_layout(title="Trilha de previsão da Coelba")
        st.plotly_chart(plot_theme(fig), use_container_width=True)

    with right:
        section_header(
            "Outliers e concentração de risco",
            "Meses em que a Coelba saiu do padrão esperado pelo modelo complementar.",
        )
        anomaly_counts = (
            coelba_ml.assign(flag_label=np.where(coelba_ml["flag_anomalia"], "Outlier", "Normal"))
            .groupby("flag_label", as_index=False)
            .size()
        )
        pie = px.pie(
            anomaly_counts,
            names="flag_label",
            values="size",
            color="flag_label",
            color_discrete_map={"Outlier": COLOR_RED, "Normal": COLOR_GREEN},
            hole=0.58,
        )
        pie.update_layout(title="Participação de meses anômalos")
        st.plotly_chart(plot_theme(pie), use_container_width=True)

    section_header(
        "Peers do mesmo cluster",
        "Distribuidoras com posicionamento semelhante ao da Coelba na camada analítica.",
    )
    cluster_value = latest_ml["cluster_performance"]
    peers = (
        ml[ml["cluster_performance"] == cluster_value]
        .groupby("distribuidora", as_index=False)
        .agg(
            score_anomalia=("score_anomalia", "mean"),
            tmae=("tmae", "mean"),
            interpretacao_cluster=("interpretacao_cluster", "first"),
        )
        .sort_values(["score_anomalia", "tmae"])
        .head(12)
    )
    st.dataframe(peers, use_container_width=True, hide_index=True)


def market_tab(data: dict[str, pd.DataFrame], filters: dict[str, list[str] | list[int]]) -> None:
    performance = apply_filters(data["performance"], filters)
    if performance.empty:
        st.warning("Sem dados para os filtros selecionados.")
        return

    latest_period = performance["data_referencia"].max()
    latest_market = performance[performance["data_referencia"] == latest_period].copy()

    left, right = st.columns((1.0, 1.0))
    with left:
        section_header(
            "Top e bottom fora do dashboard principal",
            "Leitura rápida das bordas do mercado no último período filtrado.",
        )
        ranking_slice = latest_market.sort_values("ranking_nacional")[["ranking_nacional", "distribuidora", "regiao", "tmae", "score_performance"]]
        top_bottom = pd.concat([ranking_slice.head(8), ranking_slice.tail(8)], ignore_index=True)
        st.dataframe(top_bottom, use_container_width=True, hide_index=True)

    with right:
        section_header(
            "Heatmap de quartis por região",
            "Agrupamento simples para enxergar onde se concentram faixas melhores e piores de TMAE.",
        )
        quartil_heat = (
            latest_market.groupby(["regiao", "quartil_performance"], as_index=False)
            .size()
            .pivot(index="regiao", columns="quartil_performance", values="size")
            .fillna(0)
        )
        heat = px.imshow(
            quartil_heat,
            text_auto=True,
            color_continuous_scale=[[0, "#0B3D2E"], [0.5, "#126B4D"], [1, "#00D46A"]],
            aspect="auto",
        )
        heat.update_layout(title="Quantidade de distribuidoras por quartil e região")
        st.plotly_chart(plot_theme(heat), use_container_width=True)

    section_header(
        "Composição operacional da Coelba",
        "Visão complementar de componentes para apoiar discussão gerencial fora do Power BI.",
    )
    componentes = apply_filters(data["componentes"], filters)
    comp_coelba = componentes[componentes["flag_neoenergia_coelba"]].sort_values("data_referencia")
    bars = go.Figure()
    bars.add_trace(go.Bar(x=comp_coelba["ano_mes"], y=comp_coelba["participacao_tmp"], name="TMP", marker_color=COLOR_BLUE))
    bars.add_trace(go.Bar(x=comp_coelba["ano_mes"], y=comp_coelba["participacao_tmd"], name="TMD", marker_color=COLOR_GREEN))
    bars.add_trace(go.Bar(x=comp_coelba["ano_mes"], y=comp_coelba["participacao_tme"], name="TME", marker_color=COLOR_ORANGE))
    bars.update_layout(title="Participação dos componentes do TMAE da Coelba", barmode="stack")
    st.plotly_chart(plot_theme(bars), use_container_width=True)


def architecture_tab(data: dict[str, pd.DataFrame]) -> None:
    section_header(
        "Camadas utilizadas nesta aplicação complementar",
        "A aplicação lê arquivos exportados e reutiliza a lógica herdada da modelagem dbt completa.",
    )

    catalog = [
        ("Dimension", "dim_tempo", "Calendário mensal usado para filtros globais e alinhamento temporal."),
        ("Dimension", "dim_distribuidora", "Cadastro analítico das distribuidoras, regiões e grupos econômicos."),
        ("Fact", "fct_tmae", "Fato mensal por distribuidora que sustenta a consistência da modelagem, mesmo não sendo lida diretamente pelo app."),
        ("Intermediate", "int_tmae_base_calculada", "Consolidação mensal de TMAE e componentes por distribuidora."),
        ("Intermediate", "int_tmae_benchmarks", "Médias nacionais, regionais e estatísticas de dispersão."),
        ("Intermediate", "int_tmae_ranking", "Ranking, percentil, quartil, score e distâncias para benchmark."),
        ("Intermediate", "int_tmae_evolucao", "Lag mensal/anual, média móvel e tendência da performance."),
        ("Mart", "mart_performance_tmae", "Base principal desta aplicação complementar."),
        ("Mart", "mart_componentes_tmae", "Base para decomposição do TMAE em TMP, TMD e TME."),
        ("Mart", "mart_ranking_distribuidoras", "Recorte para comparações e ranking competitivo."),
        ("Mart", "mart_ml_features_tmae", "Features para score e leitura de comportamento."),
        ("Mart", "ml_tmae_resultados", "Saída do modelo explicável de anomalia, cluster e previsão."),
    ]

    cols = st.columns(3)
    for idx, item in enumerate(catalog):
        layer, model, desc = item
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div class="catalog-card">
                    <div class="catalog-layer">{layer}</div>
                    <div class="catalog-model">{model}</div>
                    <div class="catalog-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    section_header(
        "Inventário dos arquivos de dados",
        "Visão dos arquivos utilizados pela aplicação para sustentar a análise complementar.",
    )
    inventory = []
    for name, frame in data.items():
        inventory.append(
            {
                "arquivo_dados": local_table_path(name if name != "ml_resultados" else "ml_tmae_resultados").name,
                "alias_app": name,
                "linhas": len(frame),
                "colunas": len(frame.columns),
                "inicio": frame["data_referencia"].min() if "data_referencia" in frame.columns else None,
                "fim": frame["data_referencia"].max() if "data_referencia" in frame.columns else None,
            }
        )
    inventory_df = pd.DataFrame(inventory)
    st.dataframe(inventory_df, use_container_width=True, hide_index=True)

    section_header(
        "Amostra das colunas lidas",
        "Ajuda para mostrar em reuniões quais campos sustentam a visão complementar.",
    )
    selected_table = st.selectbox("Tabela da aplicação", list(data.keys()))
    preview = pd.DataFrame({"coluna": data[selected_table].columns.tolist()})
    st.dataframe(preview, use_container_width=True, hide_index=True)


def quality_tab(data: dict[str, pd.DataFrame], filters: dict[str, list[str] | list[int]]) -> None:
    performance = apply_filters(data["performance"], filters)
    componentes = apply_filters(data["componentes"], filters)
    ml = apply_filters(data["ml_resultados"], filters)

    quality_metrics = pd.DataFrame(
        [
            {
                "checagem": "TMAE negativo",
                "resultado": int((performance["tmae"] < 0).sum()),
                "status": "OK" if int((performance["tmae"] < 0).sum()) == 0 else "Atenção",
            },
            {
                "checagem": "Datas nulas",
                "resultado": int(performance["data_referencia"].isna().sum()),
                "status": "OK" if int(performance["data_referencia"].isna().sum()) == 0 else "Atenção",
            },
            {
                "checagem": "Registros Coelba",
                "resultado": int(performance["flag_neoenergia_coelba"].sum()),
                "status": "OK" if int(performance["flag_neoenergia_coelba"].sum()) > 0 else "Falha",
            },
            {
                "checagem": "Flags de inconsistências de componentes",
                "resultado": int(componentes["flag_tmae_inconsistente"].sum()),
                "status": "OK" if int(componentes["flag_tmae_inconsistente"].sum()) == 0 else "Monitorar",
            },
            {
                "checagem": "Outliers identificados",
                "resultado": int(ml["flag_anomalia"].sum()),
                "status": "Monitorar" if int(ml["flag_anomalia"].sum()) > 0 else "OK",
            },
        ]
    )
    section_header(
        "Premissas e observabilidade",
        "Resumo das regras de negócio e de qualidade que sustentam esta visão complementar.",
    )
    st.dataframe(quality_metrics, use_container_width=True, hide_index=True)

    st.markdown(
        """
        - A aplicação usa os arquivos de dados disponíveis em `data/offline`.
        - Menor TMAE sempre representa melhor desempenho.
        - Variação negativa de TMAE representa melhora.
        - O score de performance é invertido: maior score = melhor posição relativa.
        - O uso de outliers, cluster e previsão tem papel explicativo e complementar, não substitui a leitura operacional.
        """
    )


def main() -> None:
    inject_css()
    data = load_data()
    filters = build_filters(data)
    hero(data)

    tabs = st.tabs(
        [
            "Radar complementar",
            "Previsões e risco",
            "Mercado e segmentos",
            "Arquitetura analítica",
            "Qualidade e premissas",
        ]
    )

    with tabs[0]:
        overview_tab(data, filters)
    with tabs[1]:
        forecasts_tab(data, filters)
    with tabs[2]:
        market_tab(data, filters)
    with tabs[3]:
        architecture_tab(data)
    with tabs[4]:
        quality_tab(data, filters)


if __name__ == "__main__":
    main()
