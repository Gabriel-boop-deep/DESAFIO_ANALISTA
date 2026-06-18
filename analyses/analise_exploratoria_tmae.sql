select
    data_referencia,
    regiao,
    avg(tmae) as tmae_medio,
    avg(tmp) as tmp_medio,
    avg(tmd) as tmd_medio,
    avg(tme) as tme_medio,
    count(*) as quantidade_registros
from {{ ref('mart_performance_tmae') }}
group by 1, 2
order by 1, 2

