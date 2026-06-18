with base as (
    select * from {{ ref('mart_performance_tmae') }}
),

brasil as (
    select
        data_referencia,
        avg(tmp) as tmp_brasil,
        avg(tmd) as tmd_brasil,
        avg(tme) as tme_brasil
    from base
    group by 1
)

select
    b.data_referencia,
    b.distribuidora,
    b.sigla_distribuidora,
    b.regiao,
    b.grupo_economico,
    b.flag_neoenergia_coelba,
    b.tmp,
    b.tmd,
    b.tme,
    b.tmae,
    b.participacao_tmp,
    b.participacao_tmd,
    b.participacao_tme,
    b.principal_componente_tmae,
    brasil.tmp_brasil,
    brasil.tmd_brasil,
    brasil.tme_brasil,
    b.tmp - brasil.tmp_brasil as diferenca_tmp_vs_brasil,
    b.tmd - brasil.tmd_brasil as diferenca_tmd_vs_brasil,
    b.tme - brasil.tme_brasil as diferenca_tme_vs_brasil
from base b
left join brasil using (data_referencia)

