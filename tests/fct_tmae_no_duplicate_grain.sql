select
    sk_distribuidora,
    sk_tempo,
    count(*) as total_registros
from {{ ref('fct_tmae') }}
group by 1, 2
having count(*) > 1
