with base as (
    select * from {{ ref('int_tmae_base_calculada') }}
),

distribuidora as (
    select * from {{ ref('dim_distribuidora') }}
),

tempo as (
    select * from {{ ref('dim_tempo') }}
)

select
    d.sk_distribuidora,
    t.sk_tempo,
    b.quantidade_conjuntos,
    b.tmp,
    b.tmd,
    b.tme,
    b.tmae,
    b.tmae_calculado,
    b.diferenca_tmae_calculado,
    b.flag_tmae_inconsistente,
    b.quantidade_ocorrencias,
    b.tempo_total_atendimento,
    b.flag_registro_valido
from base b
left join distribuidora d
    on b.distribuidora = d.distribuidora
   and b.sigla_distribuidora = d.sigla_distribuidora
left join tempo t
    on b.data_referencia = t.data_referencia
