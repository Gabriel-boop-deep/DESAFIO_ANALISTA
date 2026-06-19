# Guia de Montagem do Dashboard no Power BI com Base no Figma

Este guia foi escrito para montar o `.pbix` do case da Neoenergia Coelba sem alterar o layout aprovado no Figma.

Arquivos de referencia visual:
- `FIGMA/PAINEL_EXEC.png`
- `FIGMA/ranking.png`
- `FIGMA/evolucao.png`
- `FIGMA/Componentes.png`
- `FIGMA/ML.png`

Regra central:
- `menor TMAE = melhor desempenho`
- variacao negativa de TMAE = melhora
- variacao positiva de TMAE = piora

## 1. Preparacao do modelo

1. Execute `dbt run` e `dbt test`.
2. Execute `python3 scripts/train_ml_model.py` se quiser habilitar a pagina de ML.
3. No Power BI Desktop, carregue:
   - `dim_tempo`
   - `dim_distribuidora`
   - `mart_performance_tmae`
   - `mart_componentes_tmae`
   - `ml_tmae_resultados`, se existir
4. Importe o tema `powerbi/theme_neoenergia.json`.
5. Aplique os relacionamentos descritos em [relacionamentos_pbi.md](/home/nunerd/Área%20de%20trabalho/ANALISTA_DESAFIO/powerbi/relacionamentos_pbi.md:1).
6. Crie as medidas de [medidas_dax.md](/home/nunerd/Área%20de%20trabalho/ANALISTA_DESAFIO/powerbi/medidas_dax.md:1).

## 2. Regras de uso visual

- Nao altere posicao, quantidade de blocos ou identidade visual dos PNGs.
- Use os PNGs apenas como moldura de layout.
- Insira os visuais do Power BI sobre cada bloco vazio correspondente.
- Mantenha o destaque da Coelba em azul claro `#00B5E2`.
- Use verde para bom desempenho e laranja/vermelho para alerta e criticidade.

## 3. Pagina 1 - Painel Executivo

Referencia:
- `FIGMA/PAINEL_EXEC.png`

Leitura do layout:
- canto superior esquerdo: bloco grande `Principais Indicadores`
- canto superior direito: faixa horizontal curta para slicers ou resumo
- lado direito: grande painel vertical para ranking/tabela executiva
- parte inferior esquerda: grande painel para serie temporal

Passo a passo:
1. Posicione no bloco superior direito slicers compactos de `ano`, `ano_mes` e `regiao`.
2. No bloco `Principais Indicadores`, insira tres cards:
   - `TMAE Medio Coelba`
   - `Ranking Coelba`
   - `Diferenca Coelba vs Nacional`
3. Aplique cor condicional no card de diferenca:
   - verde quando negativa
   - vermelho quando positiva
4. No painel inferior esquerdo, adicione um grafico de linhas:
   - eixo: `dim_tempo[ano_mes]`
   - valores: `TMAE Medio Coelba` e `TMAE Medio Nacional`
5. No painel vertical direito, use uma tabela ou matriz com:
   - `ranking_nacional`
   - `distribuidora`
   - `tmae`
   - `diferenca_vs_brasil`
   - `classificacao_performance`
6. Aplique destaque visual para a linha da Coelba com cor de fonte ou fundo.
7. Inclua um cartao de texto pequeno com `Texto Insight Executivo`.

## 4. Pagina 2 - Ranking

Referencia:
- `FIGMA/ranking.png`

Leitura do layout:
- faixa superior inteira para slicers
- segunda faixa com cinco cards
- bloco grande central para grafico principal
- bloco grande inferior para tabela ou matriz detalhada

Passo a passo:
1. Na faixa superior, use slicers de `ano_mes`, `regiao`, `grupo_economico` e `distribuidora`.
2. Nos cinco cards, use:
   - `Ranking Coelba`
   - `Total Distribuidoras`
   - `Melhor TMAE Mercado`
   - `Pior TMAE Mercado`
   - `Quartil Desempenho Coelba`
3. No bloco central, monte barras horizontais:
   - eixo Y: `mart_performance_tmae[distribuidora]`
   - eixo X: `TMAE Medio`
   - ordenacao: crescente por TMAE
4. Use cor condicional:
   - Coelba em azul
   - demais em verde
5. No bloco inferior, crie uma matriz com:
   - `ranking_nacional`
   - `distribuidora`
   - `regiao`
   - `tmae`
   - `diferenca_vs_brasil`
   - `classificacao_performance`
   - `quartil_performance`
6. Se quiser um visual complementar, substitua a matriz por dispersao apenas se couber sem quebrar o layout.

## 5. Pagina 3 - Evolucao

Referencia:
- `FIGMA/evolucao.png`

Leitura do layout:
- cinco cards no topo
- um grande painel unico na metade inferior

Passo a passo:
1. Nos cinco cards superiores, use:
   - `TMAE Medio Coelba`
   - `TMAE Coelba Periodo Anterior`
   - `Variacao TMAE Coelba`
   - `Variacao % TMAE Coelba`
   - `Status Evolucao`
2. No painel grande inferior, use um grafico de linhas com:
   - eixo: `dim_tempo[ano_mes]`
   - valores: `TMAE Medio Coelba`, `TMAE Medio Nacional`, `Media Movel TMAE Coelba`
3. Adicione tooltip com:
   - `TMAE Coelba Ano Anterior`
   - `Variacao TMAE Coelba YoY`
   - `Tendencia Coelba`
   - `Tendencia Coelba Anual`
4. Inclua anotacao visual ou subtitle:
   - `Variacao negativa indica melhora operacional`

## 6. Pagina 4 - Componentes

Referencia:
- `FIGMA/Componentes.png`

Leitura do layout:
- tres blocos superiores de mesmo tamanho
- grande painel inferior ocupando quase toda a pagina

Uso analitico correto:
- o dataset possui componentes reais `TMP`, `TMD` e `TME`
- portanto esta pagina deve ser uma decomposicao operacional do TMAE, nao uma simulacao

Passo a passo:
1. Nos tres blocos superiores, use:
   - `Principal Componente Coelba`
   - `Quartil Desempenho Coelba`
   - `Distancia Coelba para Benchmark`
2. No grande painel inferior, use um visual de colunas empilhadas ou barras empilhadas com:
   - categoria: `dim_tempo[ano_mes]`
   - valores: `Peso TMP no TMAE`, `Peso TMD no TMAE`, `Peso TME no TMAE`
3. Se preferir, divida o painel com um combo visual usando bookmarks:
   - visao 1: participacao dos componentes
   - visao 2: comparativo Coelba vs Brasil de TMP, TMD e TME
4. Use tooltip com:
   - `TMP Coelba`
   - `TMD Coelba`
   - `TME Coelba`
   - `Gap TMP vs Brasil`
   - `Gap TMD vs Brasil`
   - `Gap TME vs Brasil`

## 7. Pagina 5 - Machine Learning

Referencia:
- `FIGMA/ML.png`

Leitura do layout:
- grade de nove blocos
- tres blocos na parte superior
- tres blocos centrais
- tres blocos inferiores

Regra de negocio:
- use apenas analise estatistica explicavel
- nada de modelo complexo sem valor claro para o case

Preenchimento recomendado:
1. Bloco 1: card `Score Performance Coelba`
2. Bloco 2: card `Cluster da Coelba`
3. Bloco 3: card `Quantidade de Outliers`
4. Bloco 4: dispersao `tmae` x `score_anomalia`
5. Bloco 5: linha `tmae` x `tmae_previsto` para Coelba
6. Bloco 6: tabela curta com distribuidoras similares por cluster
7. Bloco 7: heatmap de periodos anomalos
8. Bloco 8: ranking por `Score Performance`
9. Bloco 9: card de texto `Insight Avancado`

Se `ml_tmae_resultados` nao existir:
- mantenha a pagina como placeholder
- adicione mensagem informando que a camada depende da execucao do script de ML

## 8. Validacoes finais obrigatorias

- ranking 1 deve ser sempre o menor TMAE
- diferenca negativa vs Brasil deve ser tratada como melhora
- score maior deve indicar melhor performance
- quartil 1 deve representar melhor faixa
- outlier nao pode ser confundido com melhor desempenho
- Coelba deve aparecer em todas as paginas mesmo quando nao estiver no top 10
- sinalize no dashboard ou na apresentacao que a Coelba vai ate `2026-04-01`, enquanto a base geral vai ate `2026-05-01`

## 9. Tabelas finais recomendadas para o .pbix

- `dim_tempo`
- `dim_distribuidora`
- `mart_performance_tmae`
- `mart_componentes_tmae`
- `ml_tmae_resultados`, se existir

## 10. Estrutura sugerida da apresentacao tecnica

1. Objetivo do case e regra do TMAE
2. Fonte de dados e qualidade
3. Arquitetura dbt e BigQuery
4. Modelagem analitica
5. Painel Executivo
6. Ranking
7. Evolucao
8. Componentes
9. Analise avancada
10. Conclusoes e insights sobre a Coelba
