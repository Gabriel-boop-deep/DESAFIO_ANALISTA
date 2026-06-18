# Blueprint do Dashboard Power BI

Canvas padrao:
- Formato: `16:9`
- Tamanho: `1280 x 720 px`

Paleta Neoenergia:
- Azul principal: `#003F7D`
- Verde principal: `#00A651`
- Verde apoio: `#34B233`
- Azul claro apoio: `#00B5E2`
- Alerta: `#F28C28`
- Critico: `#D94F4F`
- Fundo: `#F5F8FB`
- Cartoes: `#FFFFFF`
- Texto principal: `#1F2D3D`
- Texto secundario: `#486581`

## Estrutura Geral

Quantidade ideal de abas: `5`

1. `Resumo Executivo`
2. `Ranking Nacional`
3. `Evolucao Temporal`
4. `Componentes TMAE`
5. `Inteligencia Analitica`

## Grade Base de Layout

Use esta grade em todas as paginas:
- Cabecalho: `1280 x 70 px`
- Filtros globais: `1280 x 70 px`
- Corpo principal: `1280 x 520 px`
- Rodape de apoio/notas: `1280 x 60 px`

Filtros globais recomendados no topo:
- `ano`
- `ano_mes`
- `regiao`
- `grupo_economico`
- `distribuidora`

## Aba 1: Resumo Executivo

Objetivo:
- mostrar rapidamente como a Coelba esta versus Brasil
- destacar tendencia, ranking e status de performance

Fonte principal:
- `mart_coelba_tmae`
- apoio: `dim_tempo`, `dim_distribuidora`

Wireframe:
- Cabecalho `1280 x 70`
  - titulo no canto esquerdo: `Desempenho Neoenergia Coelba - TMAE`
  - subtitulo no canto direito: `Menor TMAE = melhor performance`
- Filtros `1280 x 70`
- Linha de KPIs `1280 x 120`
  - KPI 1 `240 x 100`: `TMAE Medio Coelba`
  - KPI 2 `240 x 100`: `TMAE Medio Brasil`
  - KPI 3 `240 x 100`: `Diferenca Coelba vs Brasil`
  - KPI 4 `240 x 100`: `Ranking Nacional Coelba`
  - KPI 5 `240 x 100`: `Status Performance Coelba`
- Linha central `1280 x 220`
  - esquerda `760 x 220`: linha de `TMAE Coelba vs Brasil ao longo do tempo`
  - direita `500 x 220`: colunas de `Variacao Mes Anterior` + cartao de `Tendencia`
- Linha inferior `1280 x 180`
  - esquerda `620 x 180`: tabela compacta de ultimos 6 periodos
  - direita `620 x 180`: waterfall ou barras de `diferenca_vs_brasil`

## Aba 2: Ranking Nacional

Objetivo:
- responder a posicao da Coelba frente as demais distribuidoras
- identificar benchmark e pior player por periodo

Fonte principal:
- `mart_ranking_distribuidoras`
- apoio: `dim_distribuidora`, `dim_tempo`

Wireframe:
- Cabecalho `1280 x 70`
- Filtros `1280 x 70`
- Faixa superior `1280 x 110`
  - KPI 1 `250 x 90`: `Ranking Nacional Coelba`
  - KPI 2 `250 x 90`: `Ranking Regional Coelba`
  - KPI 3 `250 x 90`: `Melhor Distribuidora`
  - KPI 4 `250 x 90`: `Pior Distribuidora`
- Area principal `1280 x 340`
  - esquerda `780 x 340`: barras horizontais Top 15 distribuidoras por menor TMAE
  - direita `500 x 340`: scatter ou barras destacando Coelba, benchmark e pior distribuidora
- Area inferior `1280 x 110`
  - tabela `1280 x 110`: ranking detalhado com `distribuidora`, `tmae`, `ranking_nacional`, `diferenca_vs_brasil`

## Aba 3: Evolucao Temporal

Objetivo:
- mostrar comportamento historico do TMAE da Coelba
- evidenciar melhora, piora e estabilidade

Fonte principal:
- `mart_performance_tmae`
- filtro padrao: `flag_neoenergia_coelba = true`

Wireframe:
- Cabecalho `1280 x 70`
- Filtros `1280 x 70`
- Linha 1 `1280 x 230`
  - esquerda `820 x 230`: linha de `tmae`, `media_movel_3m` e `media_tmae_brasil`
  - direita `460 x 230`: grafico de colunas `variacao_abs_mes_anterior`
- Linha 2 `1280 x 180`
  - esquerda `420 x 180`: donut ou barra `tendencia`
  - centro `420 x 180`: cartao grande `maior melhora` e `maior piora`
  - direita `440 x 180`: matriz de `ano_mes`, `tmae`, `tmae_mes_anterior`, `variacao_pct_mes_anterior`
- Rodape `1280 x 60`
  - nota: `Variacao negativa indica melhora operacional`

## Aba 4: Componentes TMAE

Objetivo:
- entender qual componente mais puxa o TMAE
- comparar composicao da Coelba com o Brasil

Fonte principal:
- `mart_componentes_tmae`

Wireframe:
- Cabecalho `1280 x 70`
- Filtros `1280 x 70`
- Linha 1 `1280 x 120`
  - KPI 1 `300 x 100`: `TMP Medio`
  - KPI 2 `300 x 100`: `TMD Medio`
  - KPI 3 `300 x 100`: `TME Medio`
  - KPI 4 `300 x 100`: `Principal Componente`
- Linha 2 `1280 x 240`
  - esquerda `620 x 240`: barras empilhadas `participacao_tmp`, `participacao_tmd`, `participacao_tme`
  - direita `660 x 240`: colunas agrupadas `Coelba vs Brasil` para TMP, TMD e TME
- Linha 3 `1280 x 160`
  - esquerda `640 x 160`: tabela compacta com `principal_componente_tmae` por periodo
  - direita `640 x 160`: grafico de linha `diferenca_tmae_calculado` para monitorar consistencia

## Aba 5: Inteligencia Analitica

Objetivo:
- mostrar anomalias, clusters e recomendacoes

Fontes:
- `mart_ml_features_tmae`
- `ml_tmae_resultados` se a tabela ja tiver sido gerada

Wireframe:
- Cabecalho `1280 x 70`
- Filtros `1280 x 70`
- Linha 1 `1280 x 110`
  - KPI 1 `280 x 90`: `Quantidade de Anomalias`
  - KPI 2 `280 x 90`: `Percentual de Periodos Anomalos`
  - KPI 3 `280 x 90`: `Cluster da Coelba`
  - KPI 4 `380 x 90`: `Tendencia Prevista`
- Linha 2 `1280 x 240`
  - esquerda `640 x 240`: scatter de `tmae` vs `variacao_abs_mes_anterior`, cor por `cluster_performance`
  - direita `640 x 240`: linha de `tmae` vs `tmae_previsto` para Coelba
- Linha 3 `1280 x 160`
  - esquerda `520 x 160`: barras de `flag_anomalia` por periodo
  - direita `760 x 160`: tabela de `recomendacao_negocio`, `score_anomalia`, `interpretacao_cluster`

Observacao:
- se `ml_tmae_resultados` ainda nao existir, esconda temporariamente a aba 5 ou deixe uma pagina placeholder informando que a camada de ML depende da execucao de `scripts/train_ml_model.py`

