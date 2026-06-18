with base as (
    select * from {{ ref('mart_performance_tmae') }}
)

select
    data_referencia,
    distribuidora,
    sigla_distribuidora,
    regiao,
    grupo_economico,
    flag_neoenergia_coelba,
    tmp,
    tmd,
    tme,
    tmae,
    quantidade_ocorrencias,
    media_tmae_brasil,
    diferenca_vs_brasil,
    variacao_abs_mes_anterior,
    variacao_pct_mes_anterior,
    media_movel_3m,
    participacao_tmp,
    participacao_tmd,
    participacao_tme,
    principal_componente_tmae,
    ranking_nacional,
    ranking_regional,
    ranking_grupo,
    classificacao_performance
from base

