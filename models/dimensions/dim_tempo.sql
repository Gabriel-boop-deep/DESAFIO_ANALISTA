with datas as (
    select distinct data_referencia, ano, mes
    from {{ ref('stg_atendimento_emergencial') }}
    where data_referencia is not null
)

select
    {{ dbt_utils.generate_surrogate_key(['cast(data_referencia as string)']) }} as sk_tempo,
    data_referencia,
    ano,
    mes,
    format_date('%B', data_referencia) as nome_mes,
    concat('T', cast(extract(quarter from data_referencia) as string)) as trimestre,
    case when extract(month from data_referencia) <= 6 then 'S1' else 'S2' end as semestre,
    format_date('%Y-%m', data_referencia) as ano_mes
from datas
