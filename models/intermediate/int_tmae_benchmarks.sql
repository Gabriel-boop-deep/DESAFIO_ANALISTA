with base as (
    select * from {{ ref('int_tmae_base_calculada') }}
),

nacional as (
    select
        data_referencia,
        avg(tmae) as media_tmae_brasil
    from base
    group by 1
),

regional as (
    select
        data_referencia,
        regiao,
        avg(tmae) as media_tmae_regiao
    from base
    group by 1, 2
),

grupo as (
    select
        data_referencia,
        grupo_economico,
        avg(tmae) as media_tmae_grupo
    from base
    group by 1, 2
),

melhor_pior as (
    select
        data_referencia,
        array_agg(distribuidora order by tmae asc limit 1)[offset(0)] as benchmark_nacional,
        array_agg(distribuidora order by tmae asc limit 1)[offset(0)] as melhor_distribuidora_periodo,
        array_agg(distribuidora order by tmae desc limit 1)[offset(0)] as pior_distribuidora_periodo
    from base
    group by 1
)

select
    b.distribuidora,
    b.data_referencia,
    b.regiao,
    b.grupo_economico,
    n.media_tmae_brasil,
    r.media_tmae_regiao,
    g.media_tmae_grupo,
    mp.melhor_distribuidora_periodo,
    mp.pior_distribuidora_periodo,
    mp.benchmark_nacional
from base b
left join nacional n using (data_referencia)
left join regional r using (data_referencia, regiao)
left join grupo g using (data_referencia, grupo_economico)
left join melhor_pior mp using (data_referencia)

