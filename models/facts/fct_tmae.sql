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
    b.id_conjunto_unidades_consumidoras,
    b.descricao_conjunto_unidades_consumidoras,
    b.tmp,
    b.tmd,
    b.tme,
    b.tmae,
    b.quantidade_ocorrencias,
    b.tempo_total_atendimento
from base b
left join distribuidora d
    on b.distribuidora = d.distribuidora
   and b.sigla_distribuidora = d.sigla_distribuidora
left join tempo t
    on b.data_referencia = t.data_referencia

