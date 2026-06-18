# Medidas DAX

Observacao:
- as medidas que usam `ml_tmae_resultados` exigem que a tabela exista no BigQuery
- se a tabela ainda nao existir, execute `python scripts/train_ml_model.py` antes de carregar no Power BI

```DAX
TMAE Medio = AVERAGE(mart_performance_tmae[tmae])

TMP Medio = AVERAGE(mart_performance_tmae[tmp])

TMD Medio = AVERAGE(mart_performance_tmae[tmd])

TME Medio = AVERAGE(mart_performance_tmae[tme])

TMAE Medio Brasil = AVERAGE(mart_performance_tmae[media_tmae_brasil])

TMAE Medio Coelba =
CALCULATE(
    [TMAE Medio],
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Diferenca Coelba vs Brasil =
[TMAE Medio Coelba] - [TMAE Medio Brasil]

Diferenca Percentual Coelba vs Brasil =
DIVIDE([Diferenca Coelba vs Brasil], [TMAE Medio Brasil])

Ranking Nacional =
MIN(mart_performance_tmae[ranking_nacional])

Ranking Coelba =
CALCULATE(
    MIN(mart_performance_tmae[ranking_nacional]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Status Performance Coelba =
CALCULATE(
    SELECTEDVALUE(mart_performance_tmae[classificacao_performance]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Melhor Distribuidora =
SELECTEDVALUE(mart_performance_tmae[melhor_distribuidora_periodo])

Pior Distribuidora =
SELECTEDVALUE(mart_performance_tmae[pior_distribuidora_periodo])

Variacao TMAE Mes Anterior =
AVERAGE(mart_performance_tmae[variacao_abs_mes_anterior])

Variacao TMAE Mes Anterior Coelba =
CALCULATE(
    [Variacao TMAE Mes Anterior],
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Status de Performance =
SELECTEDVALUE(mart_performance_tmae[classificacao_performance])

Status Performance Coelba Texto =
CALCULATE(
    SELECTEDVALUE(mart_performance_tmae[classificacao_performance]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Principal Componente do TMAE =
SELECTEDVALUE(mart_performance_tmae[principal_componente_tmae])

Principal Componente Coelba =
CALCULATE(
    SELECTEDVALUE(mart_componentes_tmae[principal_componente_tmae]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

Quantidade de Anomalias =
CALCULATE(
    COUNTROWS(ml_tmae_resultados),
    ml_tmae_resultados[flag_anomalia] = TRUE()
)

Percentual de Periodos Anomalos =
DIVIDE(
    [Quantidade de Anomalias],
    COUNTROWS(ml_tmae_resultados)
)

Cluster da Coelba =
CALCULATE(
    SELECTEDVALUE(ml_tmae_resultados[interpretacao_cluster]),
    TREATAS(
        VALUES(mart_performance_tmae[data_referencia]),
        ml_tmae_resultados[data_referencia]
    ),
    TREATAS(
        VALUES(mart_performance_tmae[distribuidora]),
        ml_tmae_resultados[distribuidora]
    ),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Tendencia da Coelba =
CALCULATE(
    SELECTEDVALUE(mart_performance_tmae[tendencia]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Benchmark Nacional =
SELECTEDVALUE(mart_ranking_distribuidoras[benchmark_nacional])

Melhor que Brasil? =
IF(
    [Diferenca Coelba vs Brasil] < 0,
    "Melhor que o Brasil",
    IF([Diferenca Coelba vs Brasil] > 0, "Pior que o Brasil", "Igual ao Brasil")
)
```
