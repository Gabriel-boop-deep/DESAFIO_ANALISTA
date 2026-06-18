# Visuais por Pagina

## Resumo Executivo

Tabela principal:
- `mart_coelba_tmae`

Visuais:
- Cartoes:
  - `TMAE Medio Coelba`
  - `TMAE Medio Brasil`
  - `Diferenca Coelba vs Brasil`
  - `Ranking Coelba`
  - `Status Performance Coelba`
- Linha:
  - eixo: `ano_mes`
  - valores: `tmae`, `media_tmae_brasil`
- Colunas:
  - eixo: `ano_mes`
  - valor: `variacao_abs_mes_anterior`
- Tabela:
  - `ano_mes`, `tmae`, `ranking_nacional`, `diferenca_vs_brasil`, `tendencia`

## Ranking Nacional

Tabela principal:
- `mart_ranking_distribuidoras`

Visuais:
- Barras horizontais ordenadas por menor `tmae`
- Tabela ranking com:
  - `distribuidora`
  - `tmae`
  - `ranking_nacional`
  - `ranking_regional`
  - `ranking_grupo`
  - `diferenca_vs_brasil`
- Card de `benchmark_nacional`
- Card de `pior_distribuidora_periodo`

## Evolucao Temporal

Tabela principal:
- `mart_performance_tmae`

Filtro sugerido:
- `flag_neoenergia_coelba = true`

Visuais:
- Linha com `tmae`, `media_movel_3m`, `media_tmae_brasil`
- Colunas com `variacao_abs_mes_anterior`
- Matriz com `ano_mes`, `tmae`, `tmae_mes_anterior`, `variacao_pct_mes_anterior`, `tendencia`
- Donut com contagem por `tendencia`

## Componentes TMAE

Tabela principal:
- `mart_componentes_tmae`

Visuais:
- Barras empilhadas com `participacao_tmp`, `participacao_tmd`, `participacao_tme`
- Colunas agrupadas comparando `tmp` x `tmp_brasil`, `tmd` x `tmd_brasil`, `tme` x `tme_brasil`
- Tabela com `ano_mes` se derivado via dimensao de tempo, `principal_componente_tmae`, `diferenca_tmae_calculado`, `flag_tmae_inconsistente`

## Inteligencia Analitica

Tabelas:
- `mart_ml_features_tmae`
- `ml_tmae_resultados`

Visuais:
- Scatter de distribuidores por comportamento
- Linha `tmae` vs `tmae_previsto`
- Tabela de `recomendacao_negocio`
- Card de `cluster_performance`
- Card de `tendencia_prevista`

