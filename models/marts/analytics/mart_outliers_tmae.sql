select
    data_referencia,
    ano,
    mes,
    ano_mes,
    distribuidora,
    regiao,
    grupo_economico,
    tmae,
    media_tmae_brasil,
    diferenca_vs_brasil,
    zscore_tmae_brasil,
    flag_outlier_tmae,
    ranking_nacional,
    score_performance,
    classificacao_performance,
    flag_neoenergia_coelba
from {{ ref('mart_performance_tmae') }}
where flag_outlier_tmae
