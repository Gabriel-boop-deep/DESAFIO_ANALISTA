# Medidas DAX do Case Neoenergia Coelba

Premissas:
- use `mart_performance_tmae` como tabela principal do modelo
- mantenha `dim_tempo` e `dim_distribuidora` como dimensoes conectadas
- use `mart_componentes_tmae` e `ml_tmae_resultados` de forma desconectada, com `TREATAS` quando necessario
- a regra do negocio e fixa: `menor TMAE = melhor desempenho`

## Base comum

```DAX
TMAE Medio =
AVERAGE(mart_performance_tmae[tmae])

TMAE Medio Coelba =
CALCULATE(
    [TMAE Medio],
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

TMAE Medio Nacional =
AVERAGE(mart_performance_tmae[media_tmae_brasil])

TMAE Medio Regiao =
AVERAGE(mart_performance_tmae[media_tmae_regiao])

TMAE Medio Grupo =
AVERAGE(mart_performance_tmae[media_tmae_grupo])

Diferenca Coelba vs Nacional =
[TMAE Medio Coelba] - [TMAE Medio Nacional]

Diferenca % Coelba vs Nacional =
DIVIDE([Diferenca Coelba vs Nacional], [TMAE Medio Nacional])

Ranking TMAE =
MIN(mart_performance_tmae[ranking_nacional])

Ranking Coelba =
CALCULATE(
    MIN(mart_performance_tmae[ranking_nacional]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Total Distribuidoras =
MAX(mart_performance_tmae[quantidade_distribuidoras_brasil])

Melhor TMAE Mercado =
MIN(mart_performance_tmae[menor_tmae_brasil])

Pior TMAE Mercado =
MAX(mart_performance_tmae[maior_tmae_brasil])

Benchmark Nacional Nome =
CALCULATE(
    SELECTEDVALUE(mart_performance_tmae[benchmark_nacional]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Melhor Distribuidora Periodo =
CALCULATE(
    SELECTEDVALUE(mart_performance_tmae[melhor_distribuidora_periodo]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Pior Distribuidora Periodo =
CALCULATE(
    SELECTEDVALUE(mart_performance_tmae[pior_distribuidora_periodo]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Percentil Coelba =
CALCULATE(
    MIN(mart_performance_tmae[percentil_performance]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Percentil Coelba Texto =
FORMAT([Percentil Coelba], "0.0%")

Quartil Coelba =
CALCULATE(
    MIN(mart_performance_tmae[quartil_performance]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Quartil Desempenho Coelba =
SWITCH(
    [Quartil Coelba],
    1, "1o quartil - elite",
    2, "2o quartil - acima da media",
    3, "3o quartil - atencao",
    4, "4o quartil - critico",
    "Sem classificacao"
)

Distancia Coelba para Benchmark =
CALCULATE(
    AVERAGE(mart_performance_tmae[distancia_para_benchmark]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Distancia Coelba para Top 10 =
CALCULATE(
    AVERAGE(mart_performance_tmae[distancia_para_top_10]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Score Performance =
AVERAGE(mart_performance_tmae[score_performance])

Score Performance Coelba =
CALCULATE(
    [Score Performance],
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Status Desempenho Coelba =
CALCULATE(
    SELECTEDVALUE(mart_performance_tmae[classificacao_performance]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Cor Status Desempenho =
SWITCH(
    [Status Desempenho Coelba],
    "Excelente", "#00A651",
    "Bom", "#34B233",
    "Atencao", "#F28C28",
    "Critico", "#D94F4F",
    "#9AA5B1"
)

Flag Coelba =
IF(SELECTEDVALUE(mart_performance_tmae[flag_neoenergia_coelba]) = TRUE(), 1, 0)

Flag Top 10 =
IF(SELECTEDVALUE(mart_performance_tmae[flag_top_10_melhores]) = TRUE(), 1, 0)

Flag Bottom 10 =
IF(SELECTEDVALUE(mart_performance_tmae[flag_top_10_piores]) = TRUE(), 1, 0)
```

## Pagina 1 - Painel Executivo

```DAX
Texto Insight Executivo =
VAR RankingAtual = [Ranking Coelba]
VAR TotalAtual = [Total Distribuidoras]
VAR GapBrasil = [Diferenca Coelba vs Nacional]
VAR StatusAtual = [Status Desempenho Coelba]
RETURN
    "Coelba ocupa a posicao "
        & FORMAT(RankingAtual, "0")
        & " de "
        & FORMAT(TotalAtual, "0")
        & " no ranking nacional, com desempenho "
        & LOWER(StatusAtual)
        & " e gap de "
        & FORMAT(GapBrasil, "0.0")
        & " min versus a media do Brasil."

Ranking Coelba Texto =
FORMAT([Ranking Coelba], "0")
    & " / "
    & FORMAT([Total Distribuidoras], "0")

Status Ranking Coelba =
VAR Posicao = [Ranking Coelba]
RETURN
    SWITCH(
        TRUE(),
        Posicao <= 10, "Top 10 nacional",
        Posicao <= 25, "Faixa intermediaria superior",
        Posicao <= 40, "Faixa intermediaria",
        "Faixa critica"
    )
```

## Pagina 2 - Ranking

```DAX
TMAE Mediana Mercado =
MEDIAN(mart_performance_tmae[tmae])

Distancia Coelba para Melhor Distribuidora =
[Distancia Coelba para Benchmark]

Status Ranking Coelba =
VAR QuartilAtual = [Quartil Coelba]
RETURN
    SWITCH(
        QuartilAtual,
        1, "Lideranca competitiva",
        2, "Acima da mediana",
        3, "Abaixo da mediana",
        4, "Desempenho pressionado",
        "Sem classificacao"
    )

Cor Ranking Barra =
VAR DistribuidoraAtual = SELECTEDVALUE(mart_performance_tmae[distribuidora])
VAR EhCoelba =
    CALCULATE(
        MAX(mart_performance_tmae[flag_neoenergia_coelba]),
        mart_performance_tmae[distribuidora] = DistribuidoraAtual
    )
RETURN
    IF(EhCoelba = TRUE(), "#00B5E2", "#00A651")
```

## Pagina 3 - Evolucao

```DAX
TMAE Coelba Ano Anterior =
CALCULATE(
    AVERAGE(mart_performance_tmae[tmae_ano_anterior]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

TMAE Coelba Periodo Anterior =
CALCULATE(
    AVERAGE(mart_performance_tmae[tmae_mes_anterior]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Variacao TMAE Coelba =
CALCULATE(
    AVERAGE(mart_performance_tmae[variacao_abs_mes_anterior]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Variacao % TMAE Coelba =
CALCULATE(
    AVERAGE(mart_performance_tmae[variacao_pct_mes_anterior]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Variacao TMAE Coelba YoY =
CALCULATE(
    AVERAGE(mart_performance_tmae[variacao_abs_ano_anterior]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Variacao % TMAE Coelba YoY =
CALCULATE(
    AVERAGE(mart_performance_tmae[variacao_pct_ano_anterior]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

TMAE Nacional Ano Anterior =
CALCULATE(
    AVERAGE(mart_performance_tmae[media_tmae_brasil]),
    DATEADD(dim_tempo[data_referencia], -1, YEAR)
)

Gap Coelba vs Nacional =
[TMAE Medio Coelba] - [TMAE Medio Nacional]

Gap Coelba vs Nacional Ano Anterior =
[TMAE Coelba Ano Anterior] - [TMAE Nacional Ano Anterior]

Tendencia Coelba =
CALCULATE(
    SELECTEDVALUE(mart_performance_tmae[tendencia]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Tendencia Coelba Anual =
CALCULATE(
    SELECTEDVALUE(mart_performance_tmae[tendencia_anual]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Status Evolucao =
VAR VariacaoAtual = [Variacao TMAE Coelba]
RETURN
    SWITCH(
        TRUE(),
        ISBLANK(VariacaoAtual), "Sem historico",
        VariacaoAtual < 0, "Melhorou",
        VariacaoAtual > 0, "Piorou",
        "Estavel"
    )

Melhorou/Piorou/Estavel =
[Status Evolucao]

Media Movel TMAE Coelba =
CALCULATE(
    AVERAGE(mart_performance_tmae[media_movel_3m]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)
```

## Pagina 4 - Componentes

```DAX
TMP Medio =
AVERAGE(mart_componentes_tmae[tmp])

TMD Medio =
AVERAGE(mart_componentes_tmae[tmd])

TME Medio =
AVERAGE(mart_componentes_tmae[tme])

TMP Coelba =
CALCULATE(
    AVERAGE(mart_componentes_tmae[tmp]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

TMD Coelba =
CALCULATE(
    AVERAGE(mart_componentes_tmae[tmd]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

TME Coelba =
CALCULATE(
    AVERAGE(mart_componentes_tmae[tme]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

TMAE por Componente TMP =
[TMP Coelba]

TMAE por Componente TMD =
[TMD Coelba]

TMAE por Componente TME =
[TME Coelba]

Peso TMP no TMAE =
CALCULATE(
    AVERAGE(mart_componentes_tmae[participacao_tmp]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

Peso TMD no TMAE =
CALCULATE(
    AVERAGE(mart_componentes_tmae[participacao_tmd]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

Peso TME no TMAE =
CALCULATE(
    AVERAGE(mart_componentes_tmae[participacao_tme]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

Principal Componente Coelba =
CALCULATE(
    SELECTEDVALUE(mart_componentes_tmae[principal_componente_tmae]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

Gap TMP vs Brasil =
CALCULATE(
    AVERAGE(mart_componentes_tmae[diferenca_tmp_vs_brasil]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

Gap TMD vs Brasil =
CALCULATE(
    AVERAGE(mart_componentes_tmae[diferenca_tmd_vs_brasil]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

Gap TME vs Brasil =
CALCULATE(
    AVERAGE(mart_componentes_tmae[diferenca_tme_vs_brasil]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

Distancia para Benchmark Componentes =
[Distancia Coelba para Benchmark]

Score Relativo de Performance =
[Score Performance Coelba]

Classificacao Desempenho =
[Status Desempenho Coelba]
```

## Pagina 5 - Machine Learning

Observacao:
- execute `python3 scripts/train_ml_model.py` antes de usar as medidas abaixo

```DAX
Quantidade de Outliers =
CALCULATE(
    COUNTROWS(ml_tmae_resultados),
    ml_tmae_resultados[flag_anomalia] = TRUE()
)

Outliers Coelba =
CALCULATE(
    COUNTROWS(ml_tmae_resultados),
    ml_tmae_resultados[flag_anomalia] = TRUE(),
    TREATAS(
        {"Neoenergia Coelba"},
        ml_tmae_resultados[distribuidora]
    )
)

Percentual de Periodos Anomalos =
DIVIDE(
    [Quantidade de Outliers],
    COUNTROWS(ml_tmae_resultados)
)

Cluster da Coelba =
CALCULATE(
    SELECTEDVALUE(ml_tmae_resultados[cluster_performance]),
    TREATAS(
        {"Neoenergia Coelba"},
        ml_tmae_resultados[distribuidora]
    )
)

Interpretacao Cluster Coelba =
CALCULATE(
    SELECTEDVALUE(ml_tmae_resultados[interpretacao_cluster]),
    TREATAS(
        {"Neoenergia Coelba"},
        ml_tmae_resultados[distribuidora]
    )
)

Tendencia Prevista Coelba =
CALCULATE(
    SELECTEDVALUE(ml_tmae_resultados[tendencia_prevista]),
    TREATAS(
        {"Neoenergia Coelba"},
        ml_tmae_resultados[distribuidora]
    )
)

Score Anomalia Medio Coelba =
CALCULATE(
    AVERAGE(ml_tmae_resultados[score_anomalia]),
    TREATAS(
        {"Neoenergia Coelba"},
        ml_tmae_resultados[distribuidora]
    )
)

Erro Medio de Previsao Coelba =
CALCULATE(
    AVERAGE(ml_tmae_resultados[erro_previsao]),
    TREATAS(
        {"Neoenergia Coelba"},
        ml_tmae_resultados[distribuidora]
    )
)

Insight Avancado =
VAR ClusterTxt = [Interpretacao Cluster Coelba]
VAR TendenciaTxt = [Tendencia Prevista Coelba]
VAR ScoreTxt = FORMAT([Score Performance Coelba], "0.0")
RETURN
    "Coelba esta no cluster '"
        & ClusterTxt
        & "', com score de performance "
        & ScoreTxt
        & " e tendencia prevista de "
        & LOWER(TendenciaTxt)
        & "."
```
