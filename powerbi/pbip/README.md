# PBIP Base

Este diretorio contem um scaffold inicial de projeto Power BI (`PBIP`) para o dashboard da Neoenergia Coelba.

## Estrutura

```text
powerbi/pbip/
├── NeoenergiaCoelbaDashboard.pbip
├── NeoenergiaCoelbaDashboard.Report/
│   └── definition.pbir
└── NeoenergiaCoelbaDashboard.SemanticModel/
    └── definition.pbism
```

## Como usar

1. No Windows com Power BI Desktop, habilite a feature de preview `Power BI Project (.pbip) save option`.
2. Abra o arquivo:

   `powerbi/pbip/NeoenergiaCoelbaDashboard.pbip`

3. Assim que o Power BI Desktop abrir, use `Save As` no proprio projeto para que o Desktop complete/normalize os arquivos de preview que ele controla.
4. Conecte o semantic model ao BigQuery usando as tabelas do projeto:
   - `dim_tempo`
   - `dim_distribuidora`
   - `mart_performance_tmae`
   - `mart_coelba_tmae`
   - `mart_ranking_distribuidoras`
   - `mart_componentes_tmae`
   - `mart_ml_features_tmae`
   - `ml_tmae_resultados` se a camada de ML ja estiver materializada

## Observacoes

- Este scaffold foi gerado fora do Power BI Desktop e serve como ponto de partida versionavel.
- Como o recurso `PBIP` ainda esta em preview, o Power BI Desktop pode complementar ou regravar arquivos ao abrir/salvar o projeto.
- Se o Desktop acusar incompatibilidade, crie um projeto `.pbip` vazio no proprio Desktop com este mesmo nome e depois reaproveite os arquivos de tema, medidas e documentacao do diretorio `powerbi/`.
