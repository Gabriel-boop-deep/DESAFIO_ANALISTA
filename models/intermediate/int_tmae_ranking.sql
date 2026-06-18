with base as (
    select * from {{ ref('int_tmae_base_calculada') }}
)

select
    *,
    rank() over (partition by data_referencia order by tmae asc) as ranking_nacional,
    rank() over (partition by data_referencia, regiao order by tmae asc) as ranking_regional,
    rank() over (partition by data_referencia, grupo_economico order by tmae asc) as ranking_grupo,
    percent_rank() over (partition by data_referencia order by tmae asc) as percentil_performance
from base

