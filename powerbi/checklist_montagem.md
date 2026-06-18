# Checklist de Montagem no Power BI

## 1. Carga de tabelas

Carregar:
- `dim_tempo`
- `dim_distribuidora`
- `mart_performance_tmae`
- `mart_coelba_tmae`
- `mart_ranking_distribuidoras`
- `mart_componentes_tmae`
- `mart_ml_features_tmae`
- `ml_tmae_resultados` se existir

Nao carregar:
- `raw`
- `staging`
- `intermediate`

## 2. Tema visual

- importar `powerbi/theme_neoenergia.json`
- aplicar formato da pagina `16:9`
- usar fundo claro `#F5F8FB`

## 3. Relacionamentos

- criar apenas os relacionamentos descritos em `powerbi/relacionamentos_pbi.md`
- confirmar filtro em uma unica direcao

## 4. Medidas

- colar as medidas de `powerbi/medidas_dax.md`
- validar se `ml_tmae_resultados` existe antes de colar medidas de anomalia/cluster

## 5. Paginas

Criar na ordem:
1. `Resumo Executivo`
2. `Ranking Nacional`
3. `Evolucao Temporal`
4. `Componentes TMAE`
5. `Inteligencia Analitica`

## 6. Validacoes rapidas

- Coelba aparece destacada corretamente
- ranking 1 corresponde ao menor TMAE
- diferenca negativa vs Brasil indica melhor desempenho
- tendencia `Melhora` aparece quando o TMAE cai
- principal componente do TMAE muda conforme TMP/TMD/TME

## 7. Caso a camada de ML nao apareca

Se `ml_tmae_resultados` nao existir no BigQuery:
- execute `python scripts/train_ml_model.py`
- atualize o modelo no Power BI

## 8. Ordem sugerida de construcao

1. Importar tema
2. Carregar tabelas
3. Criar relacionamentos
4. Colar medidas DAX
5. Montar `Resumo Executivo`
6. Montar `Ranking Nacional`
7. Montar `Evolucao Temporal`
8. Montar `Componentes TMAE`
9. Montar `Inteligencia Analitica`

