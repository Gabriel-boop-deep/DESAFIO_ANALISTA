# Relacionamentos no Power BI

## Modelo Recomendado

Mantenha ativo apenas o modelo principal:

- `mart_performance_tmae[ano_mes]` -> `dim_tempo[ano_mes]`
- `mart_performance_tmae[distribuidora]` -> `dim_distribuidora[distribuidora]`

Cardinalidade:
- `1:*`

Direcao de filtro:
- somente da dimensao para a mart

## Relacoes que devem ficar desativadas ou nem ser criadas

- `fct_tmae` com dimensoes, se o relatorio for baseado nas marts
- `mart_coelba_tmae` com dimensoes
- `mart_componentes_tmae` com dimensoes
- `mart_ranking_distribuidoras` com dimensoes
- `mart_ml_features_tmae` com dimensoes

Motivo:
- evita caminhos ambiguos de filtro
- simplifica o comportamento dos slicers
- reduz risco de numeros divergentes entre visuais

## Quando usar `fct_tmae`

Somente se voce quiser:
- depurar granularidade
- validar a camada dimensional
- criar uma pagina tecnica

Para o dashboard executivo, prefira `mart_performance_tmae`.

## Tabela de ML

`ml_tmae_resultados`:
- deixe desconectada por padrao
- use `TREATAS` nas medidas DAX para cruzar com `mart_performance_tmae`

## Slicers recomendados

Use slicers a partir das dimensoes:
- `dim_tempo[ano]`
- `dim_tempo[ano_mes]`
- `dim_distribuidora[regiao]`
- `dim_distribuidora[grupo_economico]`
- `dim_distribuidora[distribuidora]`

