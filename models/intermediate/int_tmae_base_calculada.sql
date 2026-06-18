with base as (
    select *
    from {{ ref('stg_atendimento_emergencial') }}
    where flag_registro_valido
      and tmae is not null
),

agregada as (
    select
        distribuidora,
        sigla_distribuidora,
        max(cnpj_distribuidora) as cnpj_distribuidora,
        uf,
        regiao,
        grupo_economico,
        flag_neoenergia_coelba,
        ano,
        mes,
        data_referencia,
        count(distinct id_conjunto_unidades_consumidoras) as quantidade_conjuntos,
        sum(quantidade_ocorrencias) as quantidade_ocorrencias,
        sum(tempo_total_atendimento) as tempo_total_atendimento,
        coalesce(
            safe_divide(
                sum(case when quantidade_ocorrencias > 0 and tmp is not null then tmp * quantidade_ocorrencias end),
                sum(case when quantidade_ocorrencias > 0 and tmp is not null then quantidade_ocorrencias end)
            ),
            avg(tmp)
        ) as tmp,
        coalesce(
            safe_divide(
                sum(case when quantidade_ocorrencias > 0 and tmd is not null then tmd * quantidade_ocorrencias end),
                sum(case when quantidade_ocorrencias > 0 and tmd is not null then quantidade_ocorrencias end)
            ),
            avg(tmd)
        ) as tmd,
        coalesce(
            safe_divide(
                sum(case when quantidade_ocorrencias > 0 and tme is not null then tme * quantidade_ocorrencias end),
                sum(case when quantidade_ocorrencias > 0 and tme is not null then quantidade_ocorrencias end)
            ),
            avg(tme)
        ) as tme,
        coalesce(
            safe_divide(
                sum(case when quantidade_ocorrencias > 0 and tmae is not null then tmae * quantidade_ocorrencias end),
                sum(case when quantidade_ocorrencias > 0 and tmae is not null then quantidade_ocorrencias end)
            ),
            avg(tmae)
        ) as tmae
    from base
    group by
        distribuidora,
        sigla_distribuidora,
        uf,
        regiao,
        grupo_economico,
        flag_neoenergia_coelba,
        ano,
        mes,
        data_referencia
),

final as (
    select
        *,
        tmp + tmd + tme as tmae_calculado,
        tmae - (tmp + tmd + tme) as diferenca_tmae_calculado,
        abs(tmae - (tmp + tmd + tme)) > 0.1 as flag_tmae_inconsistente,
        tmae is not null
            and data_referencia is not null
            and quantidade_conjuntos > 0
            and not (abs(tmae - (tmp + tmd + tme)) > 0.1) as flag_registro_valido,
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
    from agregada
)

select *
from final
where flag_registro_valido
