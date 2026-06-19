with base as (
    select * from {{ ref('int_tmae_base_calculada') }}
),

posicionado as (
    select
        *,
        rank() over (partition by data_referencia order by tmae asc) as ranking_nacional,
        rank() over (partition by data_referencia, regiao order by tmae asc) as ranking_regional,
        rank() over (partition by data_referencia, grupo_economico order by tmae asc) as ranking_grupo,
        percent_rank() over (partition by data_referencia order by tmae asc) as percentil_performance,
        ntile(4) over (partition by data_referencia order by tmae asc) as quartil_performance,
        count(*) over (partition by data_referencia) as total_distribuidoras_periodo,
        min(tmae) over (partition by data_referencia) as menor_tmae_periodo,
        max(tmae) over (partition by data_referencia) as maior_tmae_periodo
    from base
),

limites as (
    select
        data_referencia,
        max(case when ranking_nacional = 1 then tmae end) as tmae_benchmark_nacional,
        max(case when ranking_nacional = least(10, total_distribuidoras_periodo) then tmae end) as tmae_limite_top_10
    from posicionado
    group by 1
)

select
    p.*,
    l.tmae_benchmark_nacional,
    l.tmae_limite_top_10,
    100 * safe_divide(
        p.maior_tmae_periodo - p.tmae,
        nullif(p.maior_tmae_periodo - p.menor_tmae_periodo, 0)
    ) as score_performance
from posicionado p
left join limites l
    using (data_referencia)
