# Imagens do Dashboard

Esta pasta concentra os PNGs exportados do dashboard final para facilitar:
- revisao visual
- versionamento dos assets
- consulta rapida durante ajustes no `.pbix` e na apresentacao

Arquivos:
- `Painel_Executivo.png`
- `RANKING.png`
- `EVOLUÇÃO.png`
- `COMPONENTES.png`
- `ML.png`

Leitura geral da qualidade visual:
- o nivel visual esta consistente com a identidade Neoenergia
- o uso da paleta verde/azul esta coerente
- a estrutura das paginas conversa bem com o layout definido no Figma

Pontos de atencao observados na revisao:
- `RANKING.png`: existem distribuidoras com `TMAE = 0,00` no topo, o que pede validacao de regra ou filtro antes de apresentar como benchmark real
- `Painel_Executivo.png`: o grafico `TMAE vs TMAE do mes anterior` pode gerar ambiguidade; para leitura executiva, a comparacao `Coelba vs media nacional` costuma ser mais clara
- `COMPONENTES.png`: o card `Quantidade de grupos economicos` nao parece ser o KPI mais forte para essa pagina; pode valer trocar por um indicador mais diretamente ligado ao TMAE
- `ML.png`: a pagina esta rica e visualmente forte, mas precisa cuidado na apresentacao para reforcar que a camada avancada e explicavel e nao decorativa

Uso recomendado:
- usar estas imagens como evidencia visual na apresentacao tecnica
- manter alinhamento entre estes PNGs, o `.pbix` final e a narrativa dos slides
