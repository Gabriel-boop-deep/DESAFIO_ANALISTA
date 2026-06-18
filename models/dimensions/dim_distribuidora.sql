select distinct
    {{ dbt_utils.generate_surrogate_key(['distribuidora', 'sigla_distribuidora']) }} as sk_distribuidora,
    distribuidora,
    sigla_distribuidora,
    uf,
    regiao,
    grupo_economico,
    flag_neoenergia_coelba
from {{ ref('stg_atendimento_emergencial') }}

