select 1
from unnest([1]) as dummy
where not exists (
    select 1
    from {{ ref('mart_performance_tmae') }}
    where flag_neoenergia_coelba
)
