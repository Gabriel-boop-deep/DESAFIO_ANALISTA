with base as (
    select * from {{ ref('int_tmae_base_calculada') }}
)

select
    *,
    lag(tmae) over (
        partition by distribuidora, id_conjunto_unidades_consumidoras
        order by data_referencia
    ) as tmae_mes_anterior,
    tmae - lag(tmae) over (
        partition by distribuidora, id_conjunto_unidades_consumidoras
        order by data_referencia
    ) as variacao_abs_mes_anterior,
    safe_divide(
        tmae - lag(tmae) over (
            partition by distribuidora, id_conjunto_unidades_consumidoras
            order by data_referencia
        ),
        lag(tmae) over (
            partition by distribuidora, id_conjunto_unidades_consumidoras
            order by data_referencia
        )
    ) as variacao_pct_mes_anterior,
    avg(tmae) over (
        partition by distribuidora, id_conjunto_unidades_consumidoras
        order by data_referencia
        rows between 2 preceding and current row
    ) as media_movel_3m,
    case
        when tmae - lag(tmae) over (
            partition by distribuidora, id_conjunto_unidades_consumidoras
            order by data_referencia
        ) <= -1 then 'Melhora'
        when tmae - lag(tmae) over (
            partition by distribuidora, id_conjunto_unidades_consumidoras
            order by data_referencia
        ) >= 1 then 'Piora'
        else 'Estavel'
    end as tendencia
from base

