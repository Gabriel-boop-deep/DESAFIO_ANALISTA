with base as (
    select *
    from {{ ref('stg_atendimento_emergencial') }}
    where not flag_registro_invalido
      and tmae is not null
),

final as (
    select
        *,
        safe_divide(tmp, nullif(tmae, 0)) as participacao_tmp,
        safe_divide(tmd, nullif(tmae, 0)) as participacao_tmd,
        safe_divide(tme, nullif(tmae, 0)) as participacao_tme,
        case
            when coalesce(tmp, -1) >= coalesce(tmd, -1)
             and coalesce(tmp, -1) >= coalesce(tme, -1) then 'Preparacao'
            when coalesce(tmd, -1) >= coalesce(tmp, -1)
             and coalesce(tmd, -1) >= coalesce(tme, -1) then 'Deslocamento'
            when coalesce(tme, -1) >= coalesce(tmp, -1)
             and coalesce(tme, -1) >= coalesce(tmd, -1) then 'Execucao'
            else 'Nao identificado'
        end as principal_componente_tmae
    from base
)

select * from final

