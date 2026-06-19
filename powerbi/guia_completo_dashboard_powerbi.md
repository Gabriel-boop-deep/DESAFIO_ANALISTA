# Guia Completo de Montagem do Dashboard Power BI

Este documento consolida em um unico lugar:
- a preparacao do modelo
- o relacionamento entre tabelas
- as medidas DAX
- o mapeamento dos blocos do Figma
- o passo a passo de montagem das paginas

Contexto do case:
- empresa foco: `Neoenergia Coelba`
- indicador principal: `TMAE`
- regra de negocio: `menor TMAE = melhor desempenho`
- variacao negativa de TMAE = melhora
- variacao positiva de TMAE = piora

Arquivos visuais do Figma analisados:
- `FIGMA/PAINEL_EXEC.png`
- `FIGMA/ranking.png`
- `FIGMA/evolucao.png`
- `FIGMA/Componentes.png`
- `FIGMA/ML.png`

## 1. Objetivo do dashboard

O dashboard deve permitir:
- comparar a Neoenergia Coelba com o mercado nacional
- entender ranking, distancia para benchmark e top 10
- acompanhar evolucao temporal do TMAE
- explicar a composicao do TMAE via `TMP`, `TMD` e `TME`
- adicionar uma camada analitica avancada, simples e explicavel

## 2. Tabelas do projeto que sustentam o Power BI

Tabelas principais para carregar no `.pbix`:
- `dim_tempo`
- `dim_distribuidora`
- `mart_performance_tmae`
- `mart_componentes_tmae`
- `ml_tmae_resultados`

Tabelas auxiliares opcionais:
- `mart_painel_executivo`
- `mart_evolucao_tmae`
- `mart_comparativo_coelba_nacional`
- `mart_score_performance`
- `mart_outliers_tmae`
- `mart_tendencia_tmae`

Recomendacao pratica:
- para o dashboard final, use principalmente `mart_performance_tmae`
- para a pagina de componentes, use `mart_componentes_tmae`
- para a pagina de ML, use `ml_tmae_resultados`

## 3. Como relacionar as tabelas no Power BI

Use como modelo principal:
- `dim_tempo[data_referencia]` -> `mart_performance_tmae[data_referencia]`
- `dim_distribuidora[distribuidora]` -> `mart_performance_tmae[distribuidora]`

Configuracao desses relacionamentos:
- cardinalidade: `1:*`
- direcao de filtro: `single`
- filtro saindo da dimensao para a mart

Tabelas que devem ficar desconectadas por padrao:
- `mart_componentes_tmae`
- `ml_tmae_resultados`
- `mart_painel_executivo`
- `mart_evolucao_tmae`
- `mart_comparativo_coelba_nacional`
- `mart_score_performance`
- `mart_outliers_tmae`
- `mart_tendencia_tmae`

Motivo:
- evita ambiguidade
- simplifica slicers
- reduz divergencia entre visuais

Como tratar a tabela `ml_tmae_resultados`:
- nao crie relacionamento fisico por padrao
- cruze com medidas DAX usando `TREATAS`

## 4. Slicers recomendados

Crie slicers a partir das dimensoes:
- `dim_tempo[ano]`
- `dim_tempo[ano_mes]`
- `dim_tempo[trimestre]`
- `dim_distribuidora[regiao]`
- `dim_distribuidora[grupo_economico]`
- `dim_distribuidora[distribuidora]`

## 5. Preparacao antes de montar o dashboard

1. Execute `dbt run`
2. Execute `dbt test`
3. Execute `python3 scripts/train_ml_model.py`
4. Abra o Power BI Desktop
5. Conecte no BigQuery
6. Carregue as tabelas listadas na secao 2
7. Importe o tema `powerbi/theme_neoenergia.json`
8. Crie os relacionamentos da secao 3
9. Crie as medidas DAX da secao 6
10. Monte as paginas conforme as secoes 7 a 11

## 6. Medidas DAX

### 6.1 Base comum

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
```

### 6.2 Painel Executivo

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
```

### 6.3 Ranking

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
```

### 6.4 Evolucao

```DAX
TMAE Coelba Periodo Anterior =
CALCULATE(
    AVERAGE(mart_performance_tmae[tmae_mes_anterior]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)

TMAE Coelba Ano Anterior =
CALCULATE(
    AVERAGE(mart_performance_tmae[tmae_ano_anterior]),
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

Media Movel TMAE Coelba =
CALCULATE(
    AVERAGE(mart_performance_tmae[media_movel_3m]),
    mart_performance_tmae[flag_neoenergia_coelba] = TRUE()
)
```

### 6.5 Componentes

```DAX
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
```

### 6.6 Machine Learning

```DAX
Quantidade de Outliers =
CALCULATE(
    COUNTROWS(ml_tmae_resultados),
    ml_tmae_resultados[flag_anomalia] = TRUE()
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

## 7. Pagina 1 - Painel Executivo

Referencia visual:
- `FIGMA/PAINEL_EXEC.png`

Blocos identificados no Figma:
- bloco grande superior esquerdo para tres indicadores
- faixa superior direita para slicers
- painel grande inferior esquerdo para grafico temporal
- painel vertical direito para ranking/tabela executiva

Como montar:
1. Coloque slicers de `ano`, `ano_mes` e `regiao` no bloco superior direito.
2. No bloco `Principais Indicadores`, coloque tres cards:
   - `TMAE Medio Coelba`
   - `Ranking Coelba`
   - `Diferenca Coelba vs Nacional`
3. No painel inferior esquerdo, insira grafico de linhas:
   - eixo: `dim_tempo[ano_mes]`
   - valores: `TMAE Medio Coelba` e `TMAE Medio Nacional`
4. No painel vertical direito, insira tabela/matriz com:
   - `ranking_nacional`
   - `distribuidora`
   - `tmae`
   - `diferenca_vs_brasil`
   - `classificacao_performance`
5. Adicione um card de texto com `Texto Insight Executivo`.

## 8. Pagina 2 - Ranking

Referencia visual:
- `FIGMA/ranking.png`

Blocos identificados no Figma:
- faixa superior para slicers
- linha de cinco cards
- um bloco central grande
- um bloco inferior grande

Como montar:
1. Na faixa superior, use slicers de `ano_mes`, `regiao`, `grupo_economico` e `distribuidora`.
2. Nos cinco cards, use:
   - `Ranking Coelba`
   - `Total Distribuidoras`
   - `Melhor TMAE Mercado`
   - `Pior TMAE Mercado`
   - `Quartil Desempenho Coelba`
3. No bloco central, use barras horizontais:
   - eixo Y: `mart_performance_tmae[distribuidora]`
   - eixo X: `TMAE Medio`
   - ordenacao crescente
4. No bloco inferior, use matriz com:
   - `ranking_nacional`
   - `distribuidora`
   - `regiao`
   - `tmae`
   - `diferenca_vs_brasil`
   - `classificacao_performance`
   - `quartil_performance`

## 9. Pagina 3 - Evolucao

Referencia visual:
- `FIGMA/evolucao.png`

Blocos identificados no Figma:
- cinco cards superiores
- um painel grande inferior

Como montar:
1. Nos cinco cards superiores, use:
   - `TMAE Medio Coelba`
   - `TMAE Coelba Periodo Anterior`
   - `Variacao TMAE Coelba`
   - `Variacao % TMAE Coelba`
   - `Status Evolucao`
2. No painel grande inferior, use grafico de linhas com:
   - `TMAE Medio Coelba`
   - `TMAE Medio Nacional`
   - `Media Movel TMAE Coelba`
3. No subtitulo ou nota visual, escreva:
   - `Variacao negativa indica melhora operacional`

## 10. Pagina 4 - Componentes

Referencia visual:
- `FIGMA/Componentes.png`

Blocos identificados no Figma:
- tres cards superiores
- um painel inferior muito grande

Leitura analitica correta:
- esta pagina deve usar os componentes reais do dataset: `TMP`, `TMD`, `TME`

Como montar:
1. Nos tres cards superiores, use:
   - `Principal Componente Coelba`
   - `Quartil Desempenho Coelba`
   - `Distancia Coelba para Benchmark`
2. No painel inferior, use barras empilhadas:
   - categoria: `dim_tempo[ano_mes]`
   - valores: `Peso TMP no TMAE`, `Peso TMD no TMAE`, `Peso TME no TMAE`
3. Se quiser enriquecer sem alterar layout, use tooltip com:
   - `TMP Coelba`
   - `TMD Coelba`
   - `TME Coelba`

## 11. Pagina 5 - Machine Learning

Referencia visual:
- `FIGMA/ML.png`

Blocos identificados no Figma:
- grade com nove blocos

Como montar:
1. Bloco 1: card `Score Performance Coelba`
2. Bloco 2: card `Cluster da Coelba`
3. Bloco 3: card `Quantidade de Outliers`
4. Bloco 4: dispersao `tmae` x `score_anomalia`
5. Bloco 5: linha `tmae` x `tmae_previsto`
6. Bloco 6: tabela de distribuidoras similares por cluster
7. Bloco 7: heatmap de meses anomalos
8. Bloco 8: ranking por score
9. Bloco 9: card textual `Insight Avancado`

## 12. Validacoes finais obrigatorias

- ranking 1 deve sempre ter o menor TMAE
- diferenca negativa vs Brasil deve indicar melhora
- score maior deve indicar melhor desempenho
- quartil 1 deve representar a melhor faixa
- Coelba deve aparecer destacada
- outlier nao significa automaticamente melhor desempenho
- a apresentacao deve sinalizar que a Coelba vai ate `2026-04-01`, enquanto a base geral vai ate `2026-05-01`

## 13. Arquivos complementares

Se quiser consultar os arquivos separados, eles continuam disponiveis em:
- `powerbi/medidas_dax.md`
- `powerbi/relacionamentos_pbi.md`
- `powerbi/guia_montagem_dashboard_figma.md`
