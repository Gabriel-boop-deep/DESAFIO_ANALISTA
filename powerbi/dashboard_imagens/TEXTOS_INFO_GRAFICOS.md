# Textos para botoes de informacao do dashboard

## Diretriz geral

Sugestao de tom para os botoes "i":
- curto
- objetivo
- explicando o que o visual mostra
- reforcando como interpretar

Frase padrao util quando fizer sentido:
`Quanto menor o TMAE, melhor o desempenho.`

---

## Menu principal

### Painel Executivo
`Apresenta uma visao geral dos principais indicadores de TMAE da Coelba, reunindo desempenho atual, comparacoes e distribuicao por grupo economico.`

### Ranking
`Permite comparar a Coelba com outras distribuidoras e identificar sua posicao relativa no indicador de TMAE.`

### Evolucao
`Mostra o comportamento historico do TMAE ao longo do tempo, destacando tendencias, variacoes e pontos de atencao.`

### Componentes
`Detalha a composicao do resultado por grupos economicos e ajuda a entender o peso de cada componente no indicador.`

### Machine Learning
`Apresenta analises avancadas para identificar clusters, anomalias e padroes que apoiam a interpretacao do desempenho.`

---

## Painel Executivo

### Card - TMAE Medio Coelba
`Mostra o valor medio do TMAE da Coelba no contexto filtrado. Este e o principal indicador de desempenho operacional apresentado na pagina.`

### Card - Ranking Coelba
`Indica a colocacao da Coelba no ranking comparativo entre distribuidoras. Posicoes melhores refletem menor TMAE em relacao aos pares.`

### Card - Coelba vs Nacional
`Mostra a diferenca entre o resultado da Coelba e a referencia nacional. Ajuda a avaliar se a empresa esta acima ou abaixo do nivel comparativo do mercado.`

### Linha - TMAE vs TMAE do mes anterior
`Compara a evolucao do TMAE atual com o periodo anterior, permitindo identificar melhora, piora ou estabilidade ao longo dos meses.`

### Treemap - TMAE por grupo economico
`Distribui o TMAE entre os grupos economicos. Areas maiores representam maior participacao no indicador e ajudam a localizar onde esta a maior concentracao do resultado.`

---

## Ranking

### Filtros
`Os filtros permitem restringir a analise por periodo, regiao, grupo economico e distribuidora, tornando a comparacao mais aderente ao contexto desejado.`

### Card - Ranking Coelba
`Mostra a posicao atual da Coelba entre as distribuidoras analisadas com base no TMAE do contexto filtrado.`

### Card - Total Distribuidoras
`Indica quantas distribuidoras fazem parte da comparacao selecionada. Esse numero ajuda a contextualizar a posicao da Coelba no ranking.`

### Card - Melhor TMAE
`Apresenta o menor TMAE encontrado entre as distribuidoras do filtro aplicado, servindo como referencia de melhor desempenho.`

### Card - Pior TMAE
`Apresenta o maior TMAE encontrado entre as distribuidoras do filtro aplicado, servindo como referencia de pior desempenho.`

### Card - Quartil Desempenho
`Classifica a Coelba em um quartil de desempenho. Quartis superiores indicam posicionamento mais competitivo em relacao aos demais participantes.`

### Barras - TMAE medio por distribuidora
`Compara o TMAE medio entre distribuidoras e facilita identificar quem apresenta melhor e pior desempenho no periodo analisado.`

### Tabela - Ranking detalhado
`Detalha a posicao de cada distribuidora, seu TMAE, a diferenca em relacao ao Brasil e a classificacao de performance, apoiando analises mais granulares.`

---

## Evolucao

### Card - TMAE Medio Coelba
`Mostra o TMAE medio da Coelba no periodo selecionado e funciona como referencia central da pagina.`

### Card - TMAE Coelba Anterior
`Apresenta o valor do periodo anterior para permitir comparacao direta com o resultado atual.`

### Card - Variacao TMAE
`Mostra a variacao absoluta entre o TMAE atual e o anterior. Valores positivos indicam aumento do indicador; valores negativos indicam reducao.`

### Card - Variacao TMAE %
`Mostra a variacao percentual do TMAE em relacao ao periodo anterior, facilitando a leitura da intensidade da mudanca.`

### Card - Status Evolucao
`Resume a leitura da tendencia recente do indicador, sinalizando de forma objetiva se o desempenho melhorou ou piorou.`

### Linha - Media TMAE Brasil e media movel 3 meses
`Exibe a serie historica do TMAE e sua suavizacao por media movel de 3 meses, ajudando a separar oscilações pontuais da tendencia principal.`

---

## Componentes

### Card - Quantidade de grupos economicos
`Informa quantos grupos economicos compoem a analise atual. Esse total ajuda a entender a amplitude da distribuicao observada na pagina.`

### Card - Evolucao
`Mostra o enquadramento atual da Coelba em faixas de desempenho, permitindo leitura rapida do posicionamento consolidado.`

### Card - Distancia para benchmarks
`Indica o quanto a Coelba ainda esta distante das referencias de melhor desempenho, apoiando a avaliacao de potencial de melhoria.`

### Colunas empilhadas - Participacao TMP, THD e TME
`Mostra como cada componente participa do resultado total ao longo do tempo. O visual ajuda a identificar quais parcelas sustentam maior peso no TMAE.`

---

## Machine Learning

### Card - Performance Coelba
`Resume o score de performance calculado pelo modelo analitico para a Coelba no contexto selecionado.`

### Card - Cluster da Coelba
`Indica em qual grupo de comportamento a Coelba foi classificada pelo modelo, considerando similaridade com outras distribuidoras.`

### Card - Outliers
`Mostra a quantidade de registros considerados fora do padrao esperado, sinalizando possiveis desvios relevantes para investigacao.`

### Tabela - TMAE x Score Anomalia
`Lista os registros com seus respectivos scores de anomalia e cluster, ajudando a identificar casos atipicos e priorizar analises.`

### Dispersao - TMAE por TMAE previsto
`Compara o valor observado com o valor previsto pelo modelo. Pontos muito distantes da tendencia podem indicar comportamento anormal ou oportunidade de investigacao.`

### Tabela - Distribuidora, cluster e interpretacao
`Apresenta a classificacao das distribuidoras por cluster e uma leitura interpretativa do perfil de performance identificado pelo modelo.`

### Dispersao - TMAE por score anomalia
`Relaciona o TMAE ao score de anomalia para destacar combinacoes de alto impacto e baixa aderencia ao comportamento esperado.`

### Colunas - Score performance por ano e mes
`Mostra a evolucao do score de performance ao longo do tempo, permitindo avaliar consistencia, ganho ou perda de desempenho segundo o modelo.`

### Card/caixa - Insight
`Apresenta uma sintese automatizada dos principais achados do modelo, traduzindo o resultado analitico em uma mensagem executiva de apoio a decisao.`

---

## Versoes mais curtas para tooltip

Se voce quiser um texto ainda menor para aparecer ao passar o mouse, pode usar este padrao:

- `Mostra o indicador principal no contexto selecionado.`
- `Compara a Coelba com distribuidoras de referencia.`
- `Exibe a tendencia historica do TMAE ao longo do tempo.`
- `Detalha a composicao do resultado por componentes.`
- `Identifica padroes, clusters e anomalias com apoio analitico.`
