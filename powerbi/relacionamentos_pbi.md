# Relacionamentos no Power BI

## Modelo recomendado

Use `mart_performance_tmae` como fato analitica principal.

Relacionamentos ativos:
- `dim_tempo[data_referencia]` -> `mart_performance_tmae[data_referencia]`
- `dim_distribuidora[distribuidora]` -> `mart_performance_tmae[distribuidora]`

Cardinalidade:
- `1:*`

Direcao de filtro:
- somente da dimensao para a fato

## Tabelas adicionais

Deixe desconectadas por padrao:
- `mart_painel_executivo`
- `mart_evolucao_tmae`
- `mart_comparativo_coelba_nacional`
- `mart_ranking_distribuidoras`
- `mart_componentes_tmae`
- `mart_score_performance`
- `mart_outliers_tmae`
- `mart_tendencia_tmae`
- `mart_ml_features_tmae`
- `ml_tmae_resultados`

Motivo:
- evita ambiguidade
- simplifica os slicers
- reduz divergencias entre paginas

## Quando usar as marts desconectadas

Use apenas se quiser:
- montar paginas muito especificas sem carregar toda a `mart_performance_tmae`
- validar resultados do dbt
- criar uma aba tecnica ou de apoio

Para o dashboard final do case, a melhor pratica e:
- visuais principais baseados em `mart_performance_tmae`
- pagina de componentes baseada em `mart_componentes_tmae`
- pagina de machine learning baseada em `ml_tmae_resultados`

## Tabela de ML

`ml_tmae_resultados`:
- deixe desconectada
- conecte a experiencia via medidas com `TREATAS`

## Slicers recomendados

Use slicers a partir das dimensoes:
- `dim_tempo[ano]`
- `dim_tempo[ano_mes]`
- `dim_tempo[trimestre]`
- `dim_distribuidora[regiao]`
- `dim_distribuidora[grupo_economico]`
- `dim_distribuidora[distribuidora]`
