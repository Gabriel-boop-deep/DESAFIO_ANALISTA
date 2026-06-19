select *
from {{ ref('mart_performance_tmae') }}
where data_referencia is null
   or extract(month from data_referencia) not between 1 and 12
   or extract(year from data_referencia) < 2000
   or extract(year from data_referencia) > extract(year from current_date())
