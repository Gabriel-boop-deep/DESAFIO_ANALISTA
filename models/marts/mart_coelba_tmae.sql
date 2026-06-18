select
    *
from {{ ref('mart_performance_tmae') }}
where flag_neoenergia_coelba

