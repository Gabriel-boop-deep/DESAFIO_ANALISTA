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

Regra obrigatoria para slicers:
- sempre prefira os campos das dimensoes para slicers globais
- nao use `ano_mes`, `regiao`, `grupo_economico` ou `distribuidora` diretamente das marts quando a dimensao equivalente existir
- isso evita conflito entre colunas homonimas em tabelas diferentes

Origem correta de cada slicer:
- `Ano` -> `dim_tempo[ano]`
- `Ano/Mes` -> `dim_tempo[ano_mes]`
- `Trimestre` -> `dim_tempo[trimestre]`
- `Regiao` -> `dim_distribuidora[regiao]`
- `Grupo Economico` -> `dim_distribuidora[grupo_economico]`
- `Distribuidora` -> `dim_distribuidora[distribuidora]`

Campos que nao devem ser usados em slicers globais, apesar de existirem em outras tabelas:
- `mart_performance_tmae[ano_mes]`
- `mart_performance_tmae[regiao]`
- `mart_performance_tmae[grupo_economico]`
- `mart_performance_tmae[distribuidora]`
- `mart_componentes_tmae[distribuidora]`
- `mart_componentes_tmae[regiao]`
- `ml_tmae_resultados[distribuidora]`

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

## 6. Como configurar valores numericos no Power BI

Esta secao existe para evitar erro comum de montagem:
- no Power BI, nao basta arrastar o campo certo
- tambem precisa definir corretamente a forma de resumo

Regra geral:
- se existir uma `medida DAX`, prefira usar a medida no visual
- use coluna bruta apenas quando o campo ja vier pronto para exibicao ou classificacao
- para cards executivos, quase sempre prefira medidas

### 6.1 Regras de agregacao

Use estas configuracoes:

| Caso | O que usar no visual | Tipo de resumo |
|---|---|---|
| KPI de TMAE | medida DAX | sem ajuste adicional |
| KPI de ranking | medida DAX | sem ajuste adicional |
| KPI de score | medida DAX | sem ajuste adicional |
| KPI de percentual | medida DAX | sem ajuste adicional |
| Serie temporal de TMAE | medida DAX | sem ajuste adicional |
| Tabela/matriz com ranking | coluna pronta da mart | `Nao resumir` |
| Tabela/matriz com nome de distribuidora | coluna pronta da mart ou dimensao | `Nao resumir` |
| Tabela/matriz com classificacao textual | coluna pronta da mart | `Nao resumir` |
| Campo numerico bruto em tabela detalhada | coluna da mart | `Nao resumir` |
| Contagem de outliers | medida DAX | sem ajuste adicional |
| Cluster | medida DAX ou coluna textual | `Nao resumir` se coluna |

### 6.2 Resumo correto por tipo de campo

Para evitar duvida, siga estas regras:

- `TMAE`, `TMP`, `TMD`, `TME` em cards e graficos:
  - usar medidas como `TMAE Medio`, `TMP Coelba`, `TMD Coelba`, `TME Coelba`
  - nao arrastar a coluna bruta e deixar o Power BI decidir

- `ranking_nacional`, `ranking_regional`, `quartil_performance`, `classificacao_performance` em tabelas:
  - usar a coluna pronta da mart
  - configurar como `Nao resumir`

- `media_tmae_brasil`, `media_movel_3m`, `score_performance` em graficos:
  - preferir medida
  - se usar coluna em tabela detalhada, manter `Nao resumir`

- `distribuidora`, `regiao`, `grupo_economico`, `ano_mes`:
  - sempre `Nao resumir`

- `flag_neoenergia_coelba`, `flag_outlier_tmae`, `flag_top_10_melhores`:
  - nao usar como card numerico bruto
  - usar em filtro, cor condicional ou medidas derivadas

### 6.3 Formato recomendado para cards e visuais

Use este padrao:

| Indicador | Formato recomendado |
|---|---|
| TMAE, TMP, TMD, TME | numero decimal com 1 ou 2 casas |
| Ranking | numero inteiro |
| Total de distribuidoras | numero inteiro |
| Distancia para benchmark/top 10 | numero decimal com 1 casa |
| Score de performance | numero decimal com 1 casa |
| Percentuais | formato percentual `%` |
| Quartil textual | texto |
| Status / classificacao | texto |

### 6.4 Como tratar percentuais no Power BI

Quando a medida representa percentual real, ha duas opcoes corretas.

Opcao preferida:
- manter a medida como numero decimal
- no menu `Modelagem`, definir o formato como `Percentual`
- ajustar casas decimais para `1` ou `2`

Exemplo:
- se a medida retorna `0,125`, o Power BI exibira `12,5%`

Use essa abordagem para:
- `Diferenca % Coelba vs Nacional`
- `Variacao % TMAE Coelba`
- `Variacao % TMAE Coelba YoY`
- medidas de participacao percentual

Opcao alternativa:
- criar uma medida textual com `FORMAT`
- usar apenas quando o card ou texto narrativo exigir composicao textual

Exemplo textual:

```DAX
Diferenca % Coelba vs Nacional Texto =
FORMAT([Diferenca % Coelba vs Nacional], "0.0%")
```

Regra importante:
- medidas formatadas como texto nao devem ser usadas em eixo numerico, ordenacao numerica ou calculos posteriores
- portanto, para graficos use a medida numerica
- para cards narrativos ou frases, pode usar a versao texto

### 6.5 Quando usar coluna bruta e quando usar medida

Use medida DAX:
- cards
- KPIs
- linhas de tendencia
- colunas agregadas
- comparativos Coelba vs Brasil
- indicadores percentuais

Use coluna bruta com `Nao resumir`:
- tabelas detalhadas
- matrizes de auditoria
- labels textuais
- classificacoes prontas da mart

### 6.6 Checklist rapido de configuracao por visual

Antes de fechar cada visual, valide:
- o campo veio da tabela certa
- se for texto, ficou `Nao resumir`
- se for ranking em tabela, ficou `Nao resumir`
- se for percentual, a medida esta como numero percentual ou texto formatado de forma consciente
- se for card numerico, preferencialmente esta usando medida e nao coluna bruta

## 7. Medidas DAX

Antes das medidas, regra de ouro de origem:
- quando houver a mesma ideia analitica em mais de uma tabela, prefira `mart_performance_tmae` como fonte principal
- use `mart_componentes_tmae` apenas para a pagina de Componentes
- use `ml_tmae_resultados` apenas para a pagina de Machine Learning

### 7.0 Mapa de origem dos indicadores

Esta secao existe para eliminar ambiguidade sobre de onde vem cada numero.

| Indicador | Tabela base | Coluna(s) base | Observacao |
|---|---|---|---|
| TMAE Medio | `mart_performance_tmae` | `tmae` | media simples no contexto do filtro |
| TMAE Medio Coelba | `mart_performance_tmae` | `tmae`, `flag_neoenergia_coelba` | filtro `TRUE()` para Coelba |
| TMAE Medio Nacional | `mart_performance_tmae` | `media_tmae_brasil` | valor ja calculado no dbt |
| Ranking Coelba | `mart_performance_tmae` | `ranking_nacional`, `flag_neoenergia_coelba` | menor ranking = melhor |
| Total Distribuidoras | `mart_performance_tmae` | `quantidade_distribuidoras_brasil` | valor ja calculado no dbt |
| Melhor TMAE Mercado | `mart_performance_tmae` | `menor_tmae_brasil` | menor TMAE do periodo |
| Pior TMAE Mercado | `mart_performance_tmae` | `maior_tmae_brasil` | maior TMAE do periodo |
| Percentil Coelba | `mart_performance_tmae` | `percentil_performance`, `flag_neoenergia_coelba` | percent rank calculado no dbt |
| Quartil Coelba | `mart_performance_tmae` | `quartil_performance`, `flag_neoenergia_coelba` | `ntile(4)` calculado no dbt |
| Distancia Coelba para Benchmark | `mart_performance_tmae` | `distancia_para_benchmark`, `flag_neoenergia_coelba` | gap entre Coelba e melhor TMAE do periodo |
| Distancia Coelba para Top 10 | `mart_performance_tmae` | `distancia_para_top_10`, `flag_neoenergia_coelba` | gap para o limite do top 10 |
| Score Performance Coelba | `mart_performance_tmae` | `score_performance`, `flag_neoenergia_coelba` | score invertido, maior = melhor |
| Status Desempenho Coelba | `mart_performance_tmae` | `classificacao_performance`, `flag_neoenergia_coelba` | `Excelente`, `Bom`, `Atencao`, `Critico` |
| TMAE Coelba Periodo Anterior | `mart_performance_tmae` | `tmae_mes_anterior`, `flag_neoenergia_coelba` | valor ja preparado no dbt |
| TMAE Coelba Ano Anterior | `mart_performance_tmae` | `tmae_ano_anterior`, `flag_neoenergia_coelba` | valor ja preparado no dbt |
| Variacao TMAE Coelba | `mart_performance_tmae` | `variacao_abs_mes_anterior`, `flag_neoenergia_coelba` | negativo = melhora |
| Variacao % TMAE Coelba | `mart_performance_tmae` | `variacao_pct_mes_anterior`, `flag_neoenergia_coelba` | negativo = melhora |
| Tendencia Coelba | `mart_performance_tmae` | `tendencia`, `flag_neoenergia_coelba` | `Melhora`, `Piora`, `Estavel` |
| Tendencia Coelba Anual | `mart_performance_tmae` | `tendencia_anual`, `flag_neoenergia_coelba` | comparacao anual |
| TMP Coelba | `mart_componentes_tmae` | `tmp`, `flag_neoenergia_coelba` | usar so na pagina Componentes |
| TMD Coelba | `mart_componentes_tmae` | `tmd`, `flag_neoenergia_coelba` | usar so na pagina Componentes |
| TME Coelba | `mart_componentes_tmae` | `tme`, `flag_neoenergia_coelba` | usar so na pagina Componentes |
| Peso TMP no TMAE | `mart_componentes_tmae` | `participacao_tmp`, `flag_neoenergia_coelba` | participacao percentual |
| Peso TMD no TMAE | `mart_componentes_tmae` | `participacao_tmd`, `flag_neoenergia_coelba` | participacao percentual |
| Peso TME no TMAE | `mart_componentes_tmae` | `participacao_tme`, `flag_neoenergia_coelba` | participacao percentual |
| Principal Componente Coelba | `mart_componentes_tmae` | `principal_componente_tmae`, `flag_neoenergia_coelba` | componente dominante |
| Quantidade de Outliers | `ml_tmae_resultados` | `flag_anomalia` | pagina ML |
| Cluster da Coelba | `ml_tmae_resultados` | `cluster_performance`, `distribuidora` | usar `TREATAS` |
| Tendencia Prevista Coelba | `ml_tmae_resultados` | `tendencia_prevista`, `distribuidora` | usar `TREATAS` |

### 7.1 Base comum

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

### 7.2 Painel Executivo

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

### 7.3 Ranking

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

### 7.4 Evolucao

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

### 7.5 Componentes

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

### 7.6 Machine Learning

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

## 8. Pagina 1 - Painel Executivo

Referencia visual:
- `FIGMA/PAINEL_EXEC.png`

Blocos identificados no Figma:
- bloco grande superior esquerdo para tres indicadores
- faixa superior direita para slicers
- painel grande inferior esquerdo para grafico temporal
- painel vertical direito para ranking/tabela executiva

Como montar:
1. Coloque slicers de `ano`, `ano_mes` e `regiao` no bloco superior direito.
   Origem exata dos slicers:
   - `ano` -> `dim_tempo[ano]`
   - `ano_mes` -> `dim_tempo[ano_mes]`
   - `regiao` -> `dim_distribuidora[regiao]`
2. No bloco `Principais Indicadores`, coloque tres cards:
   - `TMAE Medio Coelba`
   - `Ranking Coelba`
   - `Diferenca Coelba vs Nacional`
   Origem exata:
   - `TMAE Medio Coelba` -> `mart_performance_tmae[tmae]` filtrando `flag_neoenergia_coelba = TRUE()`
   - `Ranking Coelba` -> `mart_performance_tmae[ranking_nacional]` filtrando `flag_neoenergia_coelba = TRUE()`
   - `Diferenca Coelba vs Nacional` -> diferenca entre `mart_performance_tmae[tmae]` filtrado para Coelba e `mart_performance_tmae[media_tmae_brasil]`
3. No painel inferior esquerdo, insira grafico de linhas:
   - eixo: `dim_tempo[ano_mes]`
   - valores: `TMAE Medio Coelba` e `TMAE Medio Nacional`
   Origem exata:
   - serie Coelba -> `mart_performance_tmae[tmae]` com filtro `flag_neoenergia_coelba = TRUE()`
   - serie Brasil -> `mart_performance_tmae[media_tmae_brasil]`
4. No painel vertical direito, insira tabela/matriz com:
   - `ranking_nacional`
   - `distribuidora`
   - `tmae`
   - `diferenca_vs_brasil`
   - `classificacao_performance`
   Origem exata:
   - todos esses campos saem de `mart_performance_tmae`
5. Adicione um card de texto com `Texto Insight Executivo`.
   Origem exata:
   - medida DAX derivada de `Ranking Coelba`, `Total Distribuidoras`, `Diferenca Coelba vs Nacional` e `Status Desempenho Coelba`

## 9. Pagina 2 - Ranking

Referencia visual:
- `FIGMA/ranking.png`

Blocos identificados no Figma:
- faixa superior para slicers
- linha de cinco cards
- um bloco central grande
- um bloco inferior grande

Como montar:
1. Na faixa superior, use slicers de `ano_mes`, `regiao`, `grupo_economico` e `distribuidora`.
   Origem exata dos slicers:
   - `ano_mes` -> `dim_tempo[ano_mes]`
   - `regiao` -> `dim_distribuidora[regiao]`
   - `grupo_economico` -> `dim_distribuidora[grupo_economico]`
   - `distribuidora` -> `dim_distribuidora[distribuidora]`
2. Nos cinco cards, use:
   - `Ranking Coelba`
   - `Total Distribuidoras`
   - `Melhor TMAE Mercado`
   - `Pior TMAE Mercado`
   - `Quartil Desempenho Coelba`
   Origem exata:
   - todos os cinco indicadores saem de `mart_performance_tmae`
   - colunas usadas: `ranking_nacional`, `quantidade_distribuidoras_brasil`, `menor_tmae_brasil`, `maior_tmae_brasil`, `quartil_performance`
3. No bloco central, use barras horizontais:
   - eixo Y: `mart_performance_tmae[distribuidora]`
   - eixo X: `TMAE Medio`
   - ordenacao crescente
   Origem exata:
   - eixo Y -> `mart_performance_tmae[distribuidora]`
   - eixo X -> media de `mart_performance_tmae[tmae]`
4. No bloco inferior, use matriz com:
   - `ranking_nacional`
   - `distribuidora`
   - `regiao`
   - `tmae`
   - `diferenca_vs_brasil`
   - `classificacao_performance`
   - `quartil_performance`
   Origem exata:
   - todos os campos saem de `mart_performance_tmae`

## 10. Pagina 3 - Evolucao

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
   Origem exata:
   - `TMAE Medio Coelba` -> `mart_performance_tmae[tmae]`
   - `TMAE Coelba Periodo Anterior` -> `mart_performance_tmae[tmae_mes_anterior]`
   - `Variacao TMAE Coelba` -> `mart_performance_tmae[variacao_abs_mes_anterior]`
   - `Variacao % TMAE Coelba` -> `mart_performance_tmae[variacao_pct_mes_anterior]`
   - `Status Evolucao` -> medida derivada de `variacao_abs_mes_anterior`
2. No painel grande inferior, use grafico de linhas com:
   - `TMAE Medio Coelba`
   - `TMAE Medio Nacional`
   - `Media Movel TMAE Coelba`
   Origem exata:
   - Coelba -> `mart_performance_tmae[tmae]`
   - Nacional -> `mart_performance_tmae[media_tmae_brasil]`
   - media movel -> `mart_performance_tmae[media_movel_3m]`
3. No subtitulo ou nota visual, escreva:
   - `Variacao negativa indica melhora operacional`
4. Se incluir slicers nessa pagina, use apenas:
   - `dim_tempo[ano]`
   - `dim_tempo[ano_mes]`

## 11. Pagina 4 - Componentes

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
   Origem exata:
   - `Principal Componente Coelba` -> `mart_componentes_tmae[principal_componente_tmae]`
   - `Quartil Desempenho Coelba` -> `mart_performance_tmae[quartil_performance]`
   - `Distancia Coelba para Benchmark` -> `mart_performance_tmae[distancia_para_benchmark]`
2. No painel inferior, use barras empilhadas:
   - categoria: `dim_tempo[ano_mes]`
   - valores: `Peso TMP no TMAE`, `Peso TMD no TMAE`, `Peso TME no TMAE`
   Origem exata:
   - `Peso TMP no TMAE` -> `mart_componentes_tmae[participacao_tmp]`
   - `Peso TMD no TMAE` -> `mart_componentes_tmae[participacao_tmd]`
   - `Peso TME no TMAE` -> `mart_componentes_tmae[participacao_tme]`
3. Se quiser enriquecer sem alterar layout, use tooltip com:
   - `TMP Coelba`
   - `TMD Coelba`
   - `TME Coelba`
4. Se incluir slicers nessa pagina, use:
   - `dim_tempo[ano_mes]`
   - `dim_distribuidora[distribuidora]`
   Nunca use `mart_componentes_tmae[distribuidora]` como slicer global.
   Origem exata:
   - `TMP Coelba` -> `mart_componentes_tmae[tmp]`
   - `TMD Coelba` -> `mart_componentes_tmae[tmd]`
   - `TME Coelba` -> `mart_componentes_tmae[tme]`

## 12. Pagina 5 - Machine Learning

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

Origem exata por bloco:
- Bloco 1 -> `mart_performance_tmae[score_performance]` com filtro Coelba
- Bloco 2 -> `ml_tmae_resultados[cluster_performance]` com `TREATAS`
- Bloco 3 -> `ml_tmae_resultados[flag_anomalia]`
- Bloco 4 -> `ml_tmae_resultados[tmae]` x `ml_tmae_resultados[score_anomalia]`
- Bloco 5 -> `ml_tmae_resultados[tmae]` x `ml_tmae_resultados[tmae_previsto]`
- Bloco 6 -> `ml_tmae_resultados[distribuidora]`, `cluster_performance`, `interpretacao_cluster`
- Bloco 7 -> `ml_tmae_resultados[data_referencia]`, `flag_anomalia`
- Bloco 8 -> ranking sobre `mart_performance_tmae[score_performance]`
- Bloco 9 -> medida DAX textual derivada de `cluster_performance`, `tendencia_prevista` e `score_performance`

Se incluir slicers nessa pagina:
- `ano_mes` deve vir de `dim_tempo[ano_mes]`
- `distribuidora` deve vir de `dim_distribuidora[distribuidora]`
- nunca use `ml_tmae_resultados[distribuidora]` como slicer principal do relatorio

## 13. Validacoes finais obrigatorias

- ranking 1 deve sempre ter o menor TMAE
- diferenca negativa vs Brasil deve indicar melhora
- score maior deve indicar melhor desempenho
- quartil 1 deve representar a melhor faixa
- Coelba deve aparecer destacada
- outlier nao significa automaticamente melhor desempenho
- a apresentacao deve sinalizar que a Coelba vai ate `2026-04-01`, enquanto a base geral vai ate `2026-05-01`

## 14. Arquivos complementares

Se quiser consultar os arquivos separados, eles continuam disponiveis em:
- `powerbi/medidas_dax.md`
- `powerbi/relacionamentos_pbi.md`
- `powerbi/guia_montagem_dashboard_figma.md`
