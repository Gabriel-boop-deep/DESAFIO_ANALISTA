select
    data_referencia,
    distribuidora,
    id_conjunto_unidades_consumidoras,
    tmp,
    tmd,
    tme,
    tmae,
    abs((coalesce(tmp, 0) + coalesce(tmd, 0) + coalesce(tme, 0)) - tmae) as diferenca_recalculo
from {{ ref('mart_performance_tmae') }}
where abs((coalesce(tmp, 0) + coalesce(tmd, 0) + coalesce(tme, 0)) - tmae) > 0.01
order by diferenca_recalculo desc

