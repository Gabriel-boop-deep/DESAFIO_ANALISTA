# Desafio Analista Neoenergia

Projeto tecnico de Analytics Engineering para analisar a performance da Neoenergia Coelba frente as demais distribuidoras brasileiras usando BigQuery, dbt, Python e Power BI.

## Objetivo

Construir uma base analitica profissional para o indicador regulatorio TMAE, permitindo comparar a Coelba com a media nacional, acompanhar ranking, decompor o tempo em TMP/TMD/TME e adicionar uma camada interpretavel de machine learning para anomalias, clusters e tendencia.

## Arquitetura tecnica

1. CSV bruto da ANEEL em `DADOS/indicador-atendimento-emergencial.csv`.
2. `scripts/inspect_csv.py` inspeciona encoding, separador, colunas reais e gera `docs_inspecao_csv.md`.
3. `scripts/load_csv_to_bigquery.py` normaliza colunas para snake_case e carrega a tabela raw `raw_aneel.indicador_atendimento_emergencial`.
4. dbt modela staging, intermediates, dimensoes, fato e marts em `dbt_desafio_analista`.
5. `scripts/train_ml_model.py` consome `mart_performance_tmae` e grava `ml_tmae_resultados`.
6. Power BI consome `mart_performance_tmae`, `mart_coelba_tmae`, `mart_ranking_distribuidoras`, `mart_componentes_tmae` e `ml_tmae_resultados`.

## Inspecao do CSV real

- Encoding detectado: `ISO-8859-1`
- Separador detectado: `;`
- Volume inspecionado: `6.736.623` linhas de dados
- Colunas reais: `DatGeracaoConjuntoDados`, `SigAgente`, `NumCNPJ`, `IdeConjUndConsumidoras`, `DscConjUndConsumidoras`, `SigIndicador`, `AnoIndice`, `NumPeriodoIndice`, `VlrIndiceEnviado`
- O dataset vem em formato long por indicador.
- Indicadores encontrados: `TMP`, `TMD`, `TME`, `TMM`, `NumOcorr`, `Nie`, `Pnie`, `NDIACRI`, `VLCLACRI`
- Decisao tecnica: o CSV real nao traz `TMAE` explicitamente; o projeto trata `TMM` como proxy operacional de `TMAE`, validado pelo recalculo `TMP + TMD + TME`.

## Stack

- BigQuery
- dbt Core + `dbt-bigquery`
- Python 3
- pandas / numpy
- scikit-learn
- Power BI

## Estrutura de pastas

```text
.
├── README.md
├── requirements.txt
├── dbt_project.yml
├── packages.yml
├── profiles.yml.example
├── docs_inspecao_csv.md
├── analyses/
├── macros/
├── models/
├── powerbi/
└── scripts/
```

## Configuracao do ambiente

```bash
cd "/home/nunerd/Área de trabalho/ANALISTA_DESAFIO"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS="/home/nunerd/Área de trabalho/ANALISTA_DESAFIO/desafio-analista-499820-978397414cd8.json"
```

## Seguranca de credenciais

- `*.json` foi adicionado ao `.gitignore`.
- A chave da service account nao aparece em scripts nem no README alem do caminho local esperado.
- O arquivo real de profile do dbt deve ficar em `~/.dbt/profiles.yml`.
- Use `profiles.yml.example` apenas como template seguro.

## Ingestao para BigQuery

```bash
python scripts/inspect_csv.py
python scripts/load_csv_to_bigquery.py
```

O script de carga:

- detecta encoding e separador;
- padroniza colunas para snake_case;
- trata `vlr_indice_enviado` com decimal brasileiro;
- cria o dataset `raw_aneel` se necessario;
- substitui a tabela `raw_aneel.indicador_atendimento_emergencial`;
- valida a quantidade de linhas apos o load.

## Configuracao do dbt

Crie `~/.dbt/profiles.yml` a partir de `profiles.yml.example`.

```bash
cp profiles.yml.example ~/.dbt/profiles.yml
```

Depois execute:

```bash
dbt debug
dbt deps
dbt run
dbt test
dbt docs generate
dbt docs serve
```

## Camadas do modelo

- `raw`: tabela carregada diretamente do CSV real com colunas normalizadas.
- `staging`: pivot do dataset long para base por conjunto e competencia, com flags de validade e reconciliacao do TMAE.
- `intermediate`: consolidacao para uma linha por distribuidora por mes, alem das regras de benchmark, ranking, evolucao e decomposicao.
- `dimensions`: `dim_distribuidora` e `dim_tempo`.
- `facts`: `fct_tmae` em granularidade mensal por distribuidora.
- `marts`: tabelas prontas para Power BI e ML em granularidade mensal por distribuidora.

## Regras de negocio implementadas

- Menor TMAE = melhor performance.
- `ranking_nacional` com `rank() over (partition by data_referencia order by tmae asc)`.
- `diferenca_vs_brasil = tmae - media_tmae_brasil`.
- `diferenca_percentual_vs_brasil = safe_divide(tmae - media_tmae_brasil, media_tmae_brasil)`.
- Classificacao de performance com tratamento de nulos por macro `classify_performance`.
- Participacao percentual de `TMP`, `TMD` e `TME` no TMAE.
- Identificacao do principal componente do tempo.
- Evolucao mensal por distribuidora, com `Sem historico`, `Estavel`, `Melhora` e `Piora`.
- Flag robusta para identificar Neoenergia Coelba por alias.
- Validacao da composicao com `tmae_calculado`, `diferenca_tmae_calculado` e `flag_tmae_inconsistente`.
- Registros invalidos sinalizados na staging por `flag_*_valido`; apenas registros validos seguem para a camada analitica.

## Camada de machine learning

`scripts/train_ml_model.py` aplica:

- Isolation Forest para score de anomalia;
- KMeans para clusterizacao de distribuidoras;
- regressao linear temporal para tendencia prevista;
- regras de recomendacao de negocio.

Saida gerada no BigQuery:

- `dbt_desafio_analista.ml_tmae_resultados`

## Tabelas para Power BI

- `mart_performance_tmae`: tabela principal, com uma linha por distribuidora por mes.
- `mart_coelba_tmae`: foco exclusivo em Coelba.
- `mart_ranking_distribuidoras`: ranking e benchmark.
- `mart_componentes_tmae`: decomposicao do TMAE.
- `mart_ml_features_tmae`: features preparadas para ML.
- `ml_tmae_resultados`: anomalias, clusters, previsoes e recomendacoes.

## Comandos de terminal

```bash
cd "/home/nunerd/Área de trabalho/ANALISTA_DESAFIO"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS="/home/nunerd/Área de trabalho/ANALISTA_DESAFIO/desafio-analista-499820-978397414cd8.json"
python scripts/inspect_csv.py
python scripts/load_csv_to_bigquery.py
mkdir -p ~/.dbt && cp profiles.yml.example ~/.dbt/profiles.yml
dbt debug
dbt deps
dbt run
dbt test
dbt docs generate
dbt docs serve
python scripts/train_ml_model.py
```

## Premissas tecnicas

- O CSV real esta em formato long por indicador.
- `TMM` foi assumido como representacao operacional do `TMAE`.
- O mart principal foi consolidado para a granularidade `distribuidora + data_referencia`, que e a granularidade analitica esperada pelo desafio.
- `UF`, `regiao` e `grupo_economico` sao derivados heuristica e documentalmente, porque nao existem como colunas explicitas no CSV.
- `tempo_total_atendimento` e estimado por `tmae * quantidade_ocorrencias`.
- As medias Brasil, regiao e grupo economico usam media simples sobre o TMAE mensal consolidado por distribuidora. Essa premissa foi mantida por clareza e comparabilidade.

## Limitacoes

- A derivacao de `UF`, `regiao` e `grupo_economico` depende do nome do agente e pode exigir refinamento apos validacao com cadastro oficial.
- `grupo_economico` e derivado heuristica, nao vindo nativamente do CSV.
- O uso de `TMM` como proxy de `TMAE` depende da consistencia observada entre `TMM` e `TMP + TMD + TME`.
- O ambiente local precisa das dependencias Python e do acesso ao BigQuery para execucao completa.
- O modelo de ML prioriza interpretabilidade, nao a melhor acuracia estatistica possivel.
