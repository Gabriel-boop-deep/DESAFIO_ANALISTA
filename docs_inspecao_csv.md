# Inspecao do CSV de Atendimento Emergencial

## Resumo
- Arquivo: `/home/nunerd/Área de trabalho/ANALISTA_DESAFIO/DADOS/indicador-atendimento-emergencial.csv`
- Encoding detectado: `ISO-8859-1`
- Separador detectado: `;`
- Quantidade de linhas de dados: `6736663`
- Quantidade de colunas: `9`
- Linhas potencialmente malformadas: `0`

## Colunas reais

| Coluna original | Snake case sugerido | Tipo inferido | Nulos | Max len | Papel sugerido |
|---|---|---|---:|---:|---|
| DatGeracaoConjuntoDados | dat_geracao_conjunto_dados | date_string | 0 | 10 | data_geracao |
| SigAgente | sig_agente | string | 147161 | 19 | distribuidora |
| NumCNPJ | num_cnpj | numeric_string | 56856 | 14 | cnpj |
| IdeConjUndConsumidoras | ide_conj_und_consumidoras | numeric_string | 37 | 5 | id_conjunto |
| DscConjUndConsumidoras | dsc_conj_und_consumidoras | string | 37 | 37 | descricao_conjunto |
| SigIndicador | sig_indicador | string | 80 | 8 | tipo_indicador |
| AnoIndice | ano_indice | numeric_string | 80 | 4 | ano |
| NumPeriodoIndice | num_periodo_indice | numeric_string | 80 | 2 | mes |
| VlrIndiceEnviado | vlr_indice_enviado | string | 80 | 9 | valor_numerico |

## Primeiras linhas

```python
{'DatGeracaoConjuntoDados': '18-06-2026', 'SigAgente': 'ENEL CE', 'NumCNPJ': '07047251000170', 'IdeConjUndConsumidoras': '', 'DscConjUndConsumidoras': '', 'SigIndicador': 'TMP', 'AnoIndice': '2004', 'NumPeriodoIndice': '5', 'VlrIndiceEnviado': '249,70'}
{'DatGeracaoConjuntoDados': '18-06-2026', 'SigAgente': 'ENEL CE', 'NumCNPJ': '07047251000170', 'IdeConjUndConsumidoras': '', 'DscConjUndConsumidoras': '', 'SigIndicador': 'TMP', 'AnoIndice': '2004', 'NumPeriodoIndice': '6', 'VlrIndiceEnviado': '205,77'}
{'DatGeracaoConjuntoDados': '18-06-2026', 'SigAgente': 'ENEL CE', 'NumCNPJ': '07047251000170', 'IdeConjUndConsumidoras': '', 'DscConjUndConsumidoras': '', 'SigIndicador': 'TMP', 'AnoIndice': '2004', 'NumPeriodoIndice': '3', 'VlrIndiceEnviado': '242,91'}
{'DatGeracaoConjuntoDados': '18-06-2026', 'SigAgente': 'ENEL CE', 'NumCNPJ': '07047251000170', 'IdeConjUndConsumidoras': '', 'DscConjUndConsumidoras': '', 'SigIndicador': 'TMP', 'AnoIndice': '2004', 'NumPeriodoIndice': '1', 'VlrIndiceEnviado': '271,72'}
{'DatGeracaoConjuntoDados': '18-06-2026', 'SigAgente': 'ENEL CE', 'NumCNPJ': '07047251000170', 'IdeConjUndConsumidoras': '', 'DscConjUndConsumidoras': '', 'SigIndicador': 'TMP', 'AnoIndice': '2004', 'NumPeriodoIndice': '4', 'VlrIndiceEnviado': '244,93'}
```

## Nulos por coluna

- `DatGeracaoConjuntoDados`: 0
- `SigAgente`: 147161
- `NumCNPJ`: 56856
- `IdeConjUndConsumidoras`: 37
- `DscConjUndConsumidoras`: 37
- `SigIndicador`: 80
- `AnoIndice`: 80
- `NumPeriodoIndice`: 80
- `VlrIndiceEnviado`: 80

## Colunas numericas detectadas

- `NumCNPJ`, `IdeConjUndConsumidoras`, `AnoIndice`, `NumPeriodoIndice`

## Colunas com virgula decimal

- `DscConjUndConsumidoras`, `VlrIndiceEnviado`

## Indicadores encontrados

- `TMP`: 1212873
- `TMD`: 1212870
- `NumOcorr`: 1210470
- `Nie`: 1210274
- `TME`: 666058
- `Pnie`: 587766
- `TMM`: 540212
- `VLCLACRI`: 48134
- `NDIACRI`: 47926

## Distribuidoras mais frequentes

- `COELBA`: 506899
- `Neoenergia PE`: 395802
- `CEMIG-D`: 356924
- `EQUATORIAL GO`: 324514
- `COPEL-DIS`: 312542
- `COSERN`: 303786
- `CELESC`: 301347
- `EQUATORIAL PA`: 279040
- `CPFL-PAULISTA`: 235254
- `EQUATORIAL MA`: 233426
- `EMT`: 233247
- `ELEKTRO`: 231380
- `RGE`: 227744
- `RGE SUL`: 205048
- `ETO`: 196372

## Mapeamento tecnico sugerido

- `SigAgente` representa a distribuidora/agente regulado.
- `AnoIndice` e `NumPeriodoIndice` representam ano e mes de competencia.
- `SigIndicador` define o tipo de indicador, exigindo pivot em dbt.
- `VlrIndiceEnviado` armazena o valor do indicador em formato brasileiro.
- `TMM` sera tratado como proxy operacional de `TMAE`, pois o CSV real nao traz `TMAE` como sigla.
- `NumOcorr` permite derivar `quantidade_ocorrencias`.
- `tempo_total_atendimento` pode ser estimado por `tmae * quantidade_ocorrencias`.

## Campos equivalentes solicitados

- distribuidora: `SigAgente`
- uf: nao existe explicitamente no CSV; sera derivada por regra heuristica
- regiao: nao existe explicitamente no CSV; sera derivada a partir da UF quando possivel
- grupo_economico: nao existe explicitamente no CSV; sera derivado por padrao do nome da distribuidora
- ano: `AnoIndice`
- mes: `NumPeriodoIndice`
- tmp: `SigIndicador = TMP`
- tmd: `SigIndicador = TMD`
- tme: `SigIndicador = TME`
- tmae: `SigIndicador = TMM` (decisao documentada)

