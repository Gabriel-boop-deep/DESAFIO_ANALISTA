select
    data_referencia,
    distribuidora,
    sigla_distribuidora,
    uf,
    regiao,
    grupo_economico,
    tmae,
    media_tmae_brasil,
    diferenca_vs_brasil,
    ranking_nacional,
    ranking_regional,
    ranking_grupo,
    benchmark_nacional,
    melhor_distribuidora_periodo,
    pior_distribuidora_periodo,
    classificacao_performance
from {{ ref('mart_performance_tmae') }}

