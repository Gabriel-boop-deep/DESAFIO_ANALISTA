# Medidas DAX

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

Melhor Distribuidora =
SELECTEDVALUE(mart_performance_tmae[melhor_distribuidora_periodo])

Pior Distribuidora =
SELECTEDVALUE(mart_performance_tmae[pior_distribuidora_periodo])

Variacao TMAE Mes Anterior =
AVERAGE(mart_performance_tmae[variacao_abs_mes_anterior])

Status de Performance =
SELECTEDVALUE(mart_performance_tmae[classificacao_performance])

Principal Componente do TMAE =
SELECTEDVALUE(mart_performance_tmae[principal_componente_tmae])

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
    SELECTEDVALUE(ml_tmae_resultados[tendencia_prevista]),
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
```

