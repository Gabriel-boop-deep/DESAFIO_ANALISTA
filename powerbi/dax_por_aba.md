# DAX por Aba no Power BI

Este documento organiza a montagem do dashboard por pagina, usando exatamente as tabelas finais do projeto.

Recomendacao de modelo:
- Relacionamentos ativos:
  - `mart_performance_tmae[ano_mes]` -> `dim_tempo[ano_mes]`
  - `mart_performance_tmae[distribuidora]` -> `dim_distribuidora[distribuidora]`
- As demais marts podem permanecer desconectadas para evitar ambiguidade.

Observacao importante:
- As medidas que usam `ml_tmae_resultados` so funcionam se a tabela ja existir no BigQuery.
- Se necessario, execute antes:

```bash
python scripts/train_ml_model.py
```

## Aba 1: Resumo Executivo

Objetivo:
- mostrar rapidamente a performance da Neoenergia Coelba versus Brasil

Tabela principal:
- `mart_coelba_tmae`

### Medidas DAX

```DAX
TMAE Medio Coelba =
AVERAGE(mart_coelba_tmae[tmae])

TMAE Medio Brasil =
AVERAGE(mart_coelba_tmae[media_tmae_brasil])

Diferenca Coelba vs Brasil =
[TMAE Medio Coelba] - [TMAE Medio Brasil]

Diferenca Percentual Coelba vs Brasil =
DIVIDE([Diferenca Coelba vs Brasil], [TMAE Medio Brasil])

Ranking Coelba =
MIN(mart_coelba_tmae[ranking_nacional])

Status Performance Coelba =
SELECTEDVALUE(mart_coelba_tmae[classificacao_performance])

Tendencia Coelba =
SELECTEDVALUE(mart_coelba_tmae[tendencia])

Variacao TMAE Mes Anterior Coelba =
AVERAGE(mart_coelba_tmae[variacao_abs_mes_anterior])
```

### Onde vai cada coisa

- Topo da pagina:
  - slicers de `dim_tempo[ano]`, `dim_tempo[ano_mes]`, `dim_distribuidora[regiao]`
- Linha 1, cards:
  - canto superior esquerdo: `TMAE Medio Coelba`
  - centro esquerdo: `TMAE Medio Brasil`
  - centro: `Diferenca Coelba vs Brasil`
  - centro direito: `Ranking Coelba`
  - canto superior direito: `Status Performance Coelba`
- Centro esquerdo:
  - grafico de linha com `mart_coelba_tmae[ano_mes]` no eixo e `mart_coelba_tmae[tmae]`, `mart_coelba_tmae[media_tmae_brasil]` nos valores
- Centro direito:
  - card ou pequeno KPI com `Tendencia Coelba`
  - grafico de colunas com `mart_coelba_tmae[ano_mes]` e `Variacao TMAE Mes Anterior Coelba`
- Rodape:
  - tabela com `ano_mes`, `tmae`, `ranking_nacional`, `diferenca_vs_brasil`, `tendencia`

## Aba 2: Ranking Nacional

Objetivo:
- mostrar o posicionamento da Coelba e os benchmarks nacionais

Tabela principal:
- `mart_ranking_distribuidoras`

### Medidas DAX

```DAX
TMAE Medio Ranking =
AVERAGE(mart_ranking_distribuidoras[tmae])

Ranking Coelba Ranking Page =
CALCULATE(
    MIN(mart_ranking_distribuidoras[ranking_nacional]),
    mart_ranking_distribuidoras[distribuidora] = "Neoenergia Coelba"
)

Melhor Distribuidora =
SELECTEDVALUE(mart_ranking_distribuidoras[melhor_distribuidora_periodo])

Pior Distribuidora =
SELECTEDVALUE(mart_ranking_distribuidoras[pior_distribuidora_periodo])

Benchmark Nacional =
SELECTEDVALUE(mart_ranking_distribuidoras[benchmark_nacional])

Diferenca Coelba vs Brasil Ranking =
CALCULATE(
    AVERAGE(mart_ranking_distribuidoras[diferenca_vs_brasil]),
    mart_ranking_distribuidoras[distribuidora] = "Neoenergia Coelba"
)
```

### Onde vai cada coisa

- Topo:
  - slicers de `dim_tempo[ano_mes]`, `dim_distribuidora[regiao]`, `dim_distribuidora[grupo_economico]`
- Linha 1, cards:
  - esquerda: `Ranking Coelba Ranking Page`
  - centro esquerdo: `Benchmark Nacional`
  - centro direito: `Melhor Distribuidora`
  - direita: `Pior Distribuidora`
- Centro principal:
  - barras horizontais
    - eixo Y: `mart_ranking_distribuidoras[distribuidora]`
    - valor X: `mart_ranking_distribuidoras[tmae]`
    - ordenacao: crescente por `tmae`
- Lateral direita:
  - tabela curta destacando Coelba, benchmark e pior distribuidora
- Rodape:
  - tabela detalhada com `distribuidora`, `tmae`, `ranking_nacional`, `ranking_regional`, `ranking_grupo`, `diferenca_vs_brasil`

## Aba 3: Evolucao Temporal

Objetivo:
- mostrar historico, variacao e tendencia da Coelba

Tabela principal:
- `mart_performance_tmae`

Filtro visual/pagina:
- `flag_neoenergia_coelba = TRUE`

### Medidas DAX

```DAX
TMAE Medio Evolucao =
CALCULATE(
    AVERAGE(mart_performance_tmae[tmae]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Media Movel Coelba =
CALCULATE(
    AVERAGE(mart_performance_tmae[media_movel_3m]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Brasil Medio Evolucao =
CALCULATE(
    AVERAGE(mart_performance_tmae[media_tmae_brasil]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Variacao Abs Coelba =
CALCULATE(
    AVERAGE(mart_performance_tmae[variacao_abs_mes_anterior]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Variacao Pct Coelba =
CALCULATE(
    AVERAGE(mart_performance_tmae[variacao_pct_mes_anterior]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

Tendencia Atual Coelba =
CALCULATE(
    SELECTEDVALUE(mart_performance_tmae[tendencia]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)
```

### Onde vai cada coisa

- Topo:
  - slicers de `dim_tempo[ano]` e `dim_tempo[ano_mes]`
- Centro esquerdo grande:
  - grafico de linha
    - eixo: `mart_performance_tmae[ano_mes]`
    - valores: `[TMAE Medio Evolucao]`, `[Media Movel Coelba]`, `[Brasil Medio Evolucao]`
- Centro direito:
  - grafico de colunas com `[Variacao Abs Coelba]`
- Linha inferior:
  - esquerda: card `Tendencia Atual Coelba`
  - centro: card `Variacao Pct Coelba`
  - direita: matriz com `ano_mes`, `tmae_mes_anterior`, `variacao_abs_mes_anterior`, `variacao_pct_mes_anterior`, `tendencia`

## Aba 4: Componentes do TMAE

Objetivo:
- entender o peso de TMP, TMD e TME no TMAE

Tabela principal:
- `mart_componentes_tmae`

### Medidas DAX

```DAX
TMP Medio =
AVERAGE(mart_componentes_tmae[tmp])

TMD Medio =
AVERAGE(mart_componentes_tmae[tmd])

TME Medio =
AVERAGE(mart_componentes_tmae[tme])

Principal Componente Coelba =
CALCULATE(
    SELECTEDVALUE(mart_componentes_tmae[principal_componente_tmae]),
    mart_componentes_tmae[flag_neoenergia_coelba] = TRUE()
)

TMP Brasil Medio =
AVERAGE(mart_componentes_tmae[tmp_brasil])

TMD Brasil Medio =
AVERAGE(mart_componentes_tmae[tmd_brasil])

TME Brasil Medio =
AVERAGE(mart_componentes_tmae[tme_brasil])

Diferenca TMAE Calculado =
AVERAGE(mart_componentes_tmae[diferenca_tmae_calculado])
```

### Onde vai cada coisa

- Topo:
  - slicers de `dim_tempo[ano_mes]` e `dim_distribuidora[distribuidora]`
- Linha 1, cards:
  - `TMP Medio`
  - `TMD Medio`
  - `TME Medio`
  - `Principal Componente Coelba`
- Centro esquerdo:
  - barras empilhadas com `participacao_tmp`, `participacao_tmd`, `participacao_tme`
  - eixo: `mart_componentes_tmae[data_referencia]` ou `distribuidora`
- Centro direito:
  - colunas agrupadas comparando:
    - `tmp` vs `tmp_brasil`
    - `tmd` vs `tmd_brasil`
    - `tme` vs `tme_brasil`
- Rodape:
  - tabela com `distribuidora`, `principal_componente_tmae`, `diferenca_tmae_calculado`, `flag_tmae_inconsistente`

## Aba 5: Inteligencia Analitica

Objetivo:
- mostrar anomalias, clusters e previsao

Tabelas:
- `mart_ml_features_tmae`
- `ml_tmae_resultados`

### Medidas DAX

```DAX
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

Tendencia Prevista Coelba =
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

Score Medio de Anomalia =
AVERAGE(ml_tmae_resultados[score_anomalia])
```

### Onde vai cada coisa

- Topo:
  - slicers de `dim_tempo[ano_mes]` e `dim_distribuidora[distribuidora]`
- Linha 1, cards:
  - `Quantidade de Anomalias`
  - `Percentual de Periodos Anomalos`
  - `Cluster da Coelba`
  - `Tendencia Prevista Coelba`
- Centro esquerdo:
  - scatter
    - eixo X: `ml_tmae_resultados[tmae]`
    - eixo Y: `ml_tmae_resultados[score_anomalia]`
    - legenda: `ml_tmae_resultados[interpretacao_cluster]`
- Centro direito:
  - grafico de linha
    - eixo: `ml_tmae_resultados[data_referencia]`
    - valores: `ml_tmae_resultados[tmae]`, `ml_tmae_resultados[tmae_previsto]`
- Rodape:
  - tabela com `distribuidora`, `flag_anomalia`, `interpretacao_cluster`, `recomendacao_negocio`

## Ordem de Montagem Recomendada

1. `Resumo Executivo`
2. `Ranking Nacional`
3. `Evolucao Temporal`
4. `Componentes do TMAE`
5. `Inteligencia Analitica`

## Campos das Dimensoes para Slicers

Use a partir de `dim_tempo`:
- `ano`
- `ano_mes`
- `mes`

Use a partir de `dim_distribuidora`:
- `distribuidora`
- `regiao`
- `grupo_economico`
- `uf`

