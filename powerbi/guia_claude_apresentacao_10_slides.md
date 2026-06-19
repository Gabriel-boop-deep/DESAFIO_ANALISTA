# Guia para o Claude Montar a Apresentacao de 10 Slides

Este documento foi criado para servir como briefing completo para o Claude construir uma apresentacao tecnica, executiva e profissional em PowerPoint com no maximo `10 slides`.

O objetivo e garantir que a apresentacao:
- siga exatamente o contexto do case da Neoenergia Coelba
- use a logica correta do indicador `TMAE`
- reflita a modelagem real do projeto
- nao invente dados, colunas ou conclusoes
- mostre dominio tecnico, analitico e executivo

## 1. Papel esperado do Claude

O Claude deve agir como:
- um consultor senior de analytics
- um analista de negocio com visao executiva
- um storyteller tecnico

Ele deve transformar o projeto em uma apresentacao que mostre:
- clareza de raciocinio
- dominio de dados
- solidez da modelagem dbt
- preparo para Power BI
- maturidade para apresentar conclusoes a uma banca tecnica

## 2. Contexto do case

Empresa foco:
- `Neoenergia Coelba`

Objetivo do case:
- analisar a performance da Neoenergia Coelba frente as demais distribuidoras de energia do Brasil

Indicador principal:
- `TMAE — Tempo Medio de Atendimento as Emergencias`

Regra central do negocio:
- `menor TMAE = melhor desempenho operacional`
- `maior TMAE = pior desempenho operacional`

Implicacoes obrigatorias:
- ranking deve ordenar `TMAE` de forma crescente
- variacao negativa de `TMAE` representa melhora
- variacao positiva representa piora
- score de performance deve ser invertido, ou seja, menor `TMAE` gera maior score
- cores, alertas e textos devem respeitar essa regra

## 3. O que o Claude precisa saber sobre o projeto

### 3.1 Fonte de dados

Arquivo origem:
- `DADOS/indicador-atendimento-emergencial.csv`

Pontos validados:
- separador: `;`
- encoding: `ISO-8859-1`
- volume: `6.736.663` linhas
- estrutura em formato `long`
- principal chave analitica tratada no dbt: distribuidora + competencia

Indicadores encontrados no CSV:
- `TMP`
- `TMD`
- `TME`
- `TMM`
- `NumOcorr`
- `Nie`
- `Pnie`
- `NDIACRI`
- `VLCLACRI`

Decisao tecnica importante:
- o dataset nao traz `TMAE` literalmente como sigla
- o projeto trata `TMM` como proxy operacional de `TMAE`
- essa decisao foi documentada e validada pela consistencia com `TMP + TMD + TME`

### 3.2 Estrutura tecnica do projeto

Stack:
- `BigQuery`
- `dbt`
- `Power BI`
- `Python`

Camadas existentes:
- `staging`
- `intermediate`
- `dimensions`
- `facts`
- `marts`

Tabela principal para o dashboard:
- `mart_performance_tmae`

Outras tabelas relevantes:
- `dim_tempo`
- `dim_distribuidora`
- `mart_componentes_tmae`
- `ml_tmae_resultados`
- `mart_painel_executivo`
- `mart_evolucao_tmae`
- `mart_comparativo_coelba_nacional`
- `mart_score_performance`
- `mart_outliers_tmae`
- `mart_tendencia_tmae`

### 3.3 Validacao tecnica realizada

Estado final validado:
- `dbt run` executado com sucesso
- `dbt test` executado com `39/39` testes passando

Novas tabelas materializadas no BigQuery:
- `mart_painel_executivo`
- `mart_evolucao_tmae`
- `mart_comparativo_coelba_nacional`
- `mart_score_performance`
- `mart_outliers_tmae`
- `mart_tendencia_tmae`
- `ml_tmae_resultados`

Volumes validados:
- `mart_painel_executivo`: `208` linhas
- `mart_evolucao_tmae`: `208` linhas
- `mart_comparativo_coelba_nacional`: `208` linhas
- `mart_score_performance`: `20053` linhas
- `mart_outliers_tmae`: `865` linhas
- `mart_tendencia_tmae`: `20053` linhas
- `ml_tmae_resultados`: `20053` linhas

### 3.4 Restricao analitica importante

Ha uma observacao que precisa aparecer na apresentacao:
- a base geral vai ate `2026-05-01`
- a Coelba vai ate `2026-04-01`

O Claude deve tratar isso como:
- uma limitacao da cobertura do dado
- nao como erro de modelagem

## 4. Arquivos visuais que o Claude deve considerar

Os layouts do dashboard ja existem no Figma e foram analisados.

Arquivos de referencia:
- `FIGMA/PAINEL_EXEC.png`
- `FIGMA/ranking.png`
- `FIGMA/evolucao.png`
- `FIGMA/Componentes.png`
- `FIGMA/ML.png`

O Claude nao deve propor novas paginas de dashboard.

Ele deve assumir que a apresentacao vai:
- mostrar a logica do projeto
- explicar como o dashboard foi estruturado
- contar a historia executiva da Coelba com base nessas cinco visoes

## 5. Estilo da apresentacao

O tom deve ser:
- profissional
- seguro
- tecnico, mas acessivel
- executivo

O estilo nao deve ser:
- academico demais
- prolixo
- genrico
- excessivamente marketing

A apresentacao precisa parecer feita por alguem que:
- entende dbt
- entende modelagem analitica
- entende Power BI
- entende indicadores regulatorios
- sabe transformar dado em narrativa executiva

## 6. Objetivo narrativo da apresentacao

O fio condutor sugerido para o Claude e:

1. contextualizar o problema de negocio
2. explicar a fonte e os cuidados com os dados
3. mostrar a arquitetura tecnica e a modelagem
4. evidenciar o racional analitico do TMAE
5. apresentar a visao executiva da Coelba
6. mostrar comparacao com o mercado
7. mostrar evolucao temporal
8. explicar os componentes operacionais do indicador
9. trazer uma camada analitica avancada explicavel
10. fechar com conclusoes e recomendacoes

## 7. O que o Claude nao pode fazer

O Claude nao pode:
- inventar numeros
- inventar distribuidoras
- inventar colunas
- inventar tecnicas de machine learning sem base no projeto
- inverter a regra do `TMAE`
- tratar variacao positiva como melhora
- dizer que `TMAE` alto e bom
- omitir a limitacao temporal da Coelba
- criar mais de `10 slides`

## 8. Estrutura exata sugerida de 10 slides

O Claude deve montar os 10 slides usando a estrutura abaixo.

### Slide 1 - Capa

Objetivo:
- abrir a apresentacao com clareza e posicionamento profissional

Conteudo esperado:
- titulo do case
- subtitulo com objetivo da analise
- nome do candidato
- vaga ou contexto da Neoenergia Coelba

Mensagem principal:
- a apresentacao mostra como a performance da Coelba foi analisada frente ao mercado usando `dbt`, `BigQuery` e `Power BI`

### Slide 2 - Contexto de negocio e regra do indicador

Objetivo:
- explicar o problema de negocio antes da tecnica

Conteudo esperado:
- o que e `TMAE`
- por que ele importa operacionalmente
- regra obrigatoria: `menor TMAE = melhor`
- o que a analise precisa responder sobre a Coelba

Mensagem principal:
- toda a leitura do dashboard depende da interpretacao correta do indicador

### Slide 3 - Fonte de dados e qualidade

Objetivo:
- mostrar rigor tecnico com a origem

Conteudo esperado:
- origem do CSV
- formato long
- encoding e separador
- volume de linhas
- principais indicadores encontrados
- decisao de tratar `TMM` como proxy de `TMAE`
- principais testes de qualidade aplicados

Mensagem principal:
- a confiabilidade do dashboard dependeu de uma etapa cuidadosa de inspeção, padronizacao e validacao do dado

### Slide 4 - Arquitetura tecnica e modelagem dbt

Objetivo:
- demonstrar maturidade de engenharia analitica

Conteudo esperado:
- fluxo `CSV -> BigQuery -> dbt -> marts -> Power BI`
- separacao entre `staging`, `intermediate`, `dimensions`, `facts` e `marts`
- papel da `mart_performance_tmae`
- dimensoes principais
- testes e documentacao

Mensagem principal:
- o projeto nao foi apenas um dashboard; foi uma base analitica estruturada para consumo confiavel

### Slide 5 - Logica analitica aplicada ao TMAE

Objetivo:
- mostrar que a regra de negocio foi corretamente traduzida em metrica

Conteudo esperado:
- TMAE medio por distribuidora
- media nacional
- ranking nacional crescente
- comparacao Coelba vs Brasil
- variacao mensal e anual
- score invertido de performance
- percentil, quartil e distancia ao benchmark/top 10

Mensagem principal:
- a modelagem foi desenhada para responder perguntas executivas sem deixar a logica toda para o Power BI

### Slide 6 - Visao executiva da Coelba

Objetivo:
- apresentar a pagina `Painel Executivo`

Conteudo esperado:
- quais KPIs entram na aba
- o que a pagina responde
- como a Coelba e comparada ao Brasil
- destaque para `TMAE Medio Coelba`, `Ranking Coelba` e `Gap vs Nacional`

Mensagem principal:
- o painel executivo entrega uma leitura rapida do posicionamento atual da Coelba

### Slide 7 - Comparativo competitivo e ranking

Objetivo:
- apresentar a pagina `Ranking`

Conteudo esperado:
- comparacao entre distribuidoras
- posicao da Coelba
- melhor e pior desempenho
- quartil e percentil da Coelba
- distancia da Coelba para o benchmark e para o top 10

Mensagem principal:
- o ranking traduz a posicao relativa da Coelba no mercado de forma objetiva

### Slide 8 - Evolucao temporal e componentes do indicador

Objetivo:
- combinar as paginas `Evolucao` e `Componentes`

Conteudo esperado:
- linha temporal Coelba vs Brasil
- media movel
- leitura de melhora/piora
- decomposicao por `TMP`, `TMD` e `TME`
- principal componente do TMAE

Mensagem principal:
- alem de saber se a Coelba esta bem ou mal, a analise mostra como esse desempenho evolui e quais componentes puxam o indicador

### Slide 9 - Analise avancada explicavel

Objetivo:
- apresentar a camada de ML/analitica avancada sem exagero

Conteudo esperado:
- score de performance
- outliers
- cluster da Coelba
- tendencia prevista
- racional de negocio dessas tecnicas

Mensagem principal:
- a camada avancada foi pensada para ampliar interpretabilidade e priorizacao, nao para parecer complexa artificialmente

### Slide 10 - Conclusoes, limitacoes e recomendacoes

Objetivo:
- encerrar com maturidade executiva

Conteudo esperado:
- principais achados sobre a posicao da Coelba
- o que o dashboard permite monitorar
- principal limitacao temporal da base
- recomendacoes de evolucao analitica

Mensagem principal:
- a entrega combina robustez tecnica com aplicabilidade executiva para apoiar leitura comparativa da Coelba frente ao setor

## 9. O que deve aparecer como diferencial competitivo

O Claude deve valorizar estes pontos:
- inspecao e tratamento serio da fonte
- modelagem em camadas no dbt
- testes de qualidade
- tabelas finais prontas para Power BI
- separacao entre logica de dados e logica de visualizacao
- score invertido coerente com o negocio
- outliers e clustering explicaveis
- preocupacao com leitura executiva

## 10. Tom das conclusoes

As conclusoes devem soar como:
- analiticas
- prudentes
- orientadas ao negocio

Nao devem soar como:
- chute
- frase vazia
- certeza absoluta sem base

O Claude deve usar formulacoes como:
- `a modelagem foi estruturada para...`
- `o dashboard permite identificar...`
- `a leitura comparativa mostra...`
- `uma limitacao relevante da base e...`
- `como proximo passo, seria recomendavel...`

## 11. Se o Claude quiser incluir apoio visual

Ele pode sugerir em cada slide:
- pequenos mockups do dashboard
- diagramas simples de arquitetura
- tabelas-resumo
- bullets curtos

Mas deve evitar:
- slides lotados
- textos longos
- excesso de tabelas
- prints sem legenda

## 12. Resultado esperado

Ao final, o Claude deve produzir:
- uma estrutura completa de `10 slides`
- titulo e objetivo de cada slide
- bullets principais
- narrativa coerente entre inicio, meio e fim
- linguagem profissional
- alinhamento real com o projeto entregue

## 13. Arquivos de apoio do projeto

Se o Claude quiser referenciar os artefatos do projeto, os principais sao:
- `powerbi/guia_completo_dashboard_powerbi.md`
- `powerbi/medidas_dax.md`
- `powerbi/guia_montagem_dashboard_figma.md`
- `powerbi/relacionamentos_pbi.md`
- `models/marts/mart_performance_tmae.sql`
- `models/marts/mart_componentes_tmae.sql`
- `models/intermediate/int_tmae_ranking.sql`

## 14. Instrucao final ao Claude

Monte a apresentacao como se ela fosse ser avaliada por uma banca tecnica da Neoenergia.

Ela precisa transmitir, ao mesmo tempo:
- dominio tecnico
- clareza de negocio
- capacidade executiva
- criterio analitico

Nao invente dados.
Nao ultrapasse `10 slides`.
Nao quebre a logica do `TMAE`.
Use o projeto real como base.
