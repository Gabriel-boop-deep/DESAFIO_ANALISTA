with raw as (
    select
        parse_date('%d-%m-%Y', dat_geracao_conjunto_dados) as data_geracao_conjunto,
        upper(trim(sig_agente)) as distribuidora_raw,
        cast(num_cnpj as string) as cnpj_distribuidora,
        safe_cast(ide_conj_und_consumidoras as int64) as id_conjunto_unidades_consumidoras,
        nullif(upper(trim(dsc_conj_und_consumidoras)), '') as descricao_conjunto_unidades_consumidoras,
        upper(trim(sig_indicador)) as sig_indicador,
        safe_cast(ano_indice as int64) as ano,
        safe_cast(num_periodo_indice as int64) as mes,
        safe_cast(vlr_indice_enviado as float64) as valor_indicador
    from {{ source('raw_aneel', 'indicador_atendimento_emergencial') }}
    where safe_cast(ano_indice as int64) is not null
      and safe_cast(num_periodo_indice as int64) between 1 and 12
),

enriched as (
    select
        data_geracao_conjunto,
        distribuidora_raw,
        case
            when regexp_contains(distribuidora_raw, r'COELBA|NEOENERGIA COELBA|COMPANHIA DE ELETRICIDADE DO ESTADO DA BAHIA|CIA DE ELETRICIDADE DO ESTADO DA BAHIA')
                then 'Neoenergia Coelba'
            when regexp_contains(distribuidora_raw, r'COSERN')
                then 'Neoenergia Cosern'
            when regexp_contains(distribuidora_raw, r'NEOENERGIA PE|CELPE')
                then 'Neoenergia Pernambuco'
            when regexp_contains(distribuidora_raw, r'NEOENERGIA BRASILIA')
                then 'Neoenergia Brasilia'
            else initcap(lower(distribuidora_raw))
        end as distribuidora,
        distribuidora_raw as sigla_distribuidora,
        cnpj_distribuidora,
        id_conjunto_unidades_consumidoras,
        descricao_conjunto_unidades_consumidoras,
        sig_indicador,
        ano,
        mes,
        date(ano, mes, 1) as data_referencia,
        valor_indicador,
        case
            when regexp_contains(distribuidora_raw, r'COELBA|NEOENERGIA COELBA|COMPANHIA DE ELETRICIDADE DO ESTADO DA BAHIA|CIA DE ELETRICIDADE DO ESTADO DA BAHIA') then 'BA'
            when regexp_contains(distribuidora_raw, r'COSERN') then 'RN'
            when regexp_contains(distribuidora_raw, r'NEOENERGIA PE|CELPE') then 'PE'
            when regexp_contains(distribuidora_raw, r'NEOENERGIA BRASILIA') then 'DF'
            when regexp_contains(distribuidora_raw, r'EQUATORIAL AL') then 'AL'
            when regexp_contains(distribuidora_raw, r'EQUATORIAL GO') then 'GO'
            when regexp_contains(distribuidora_raw, r'EQUATORIAL MA') then 'MA'
            when regexp_contains(distribuidora_raw, r'EQUATORIAL PA') then 'PA'
            when regexp_contains(distribuidora_raw, r'EQUATORIAL PI') then 'PI'
            when regexp_contains(distribuidora_raw, r'ENEL CE') then 'CE'
            when regexp_contains(distribuidora_raw, r'ENEL RJ') then 'RJ'
            when regexp_contains(distribuidora_raw, r'EDP ES') then 'ES'
            when regexp_contains(distribuidora_raw, r'EDP SP') then 'SP'
            when regexp_contains(distribuidora_raw, r'CPFL-PAULISTA|CPFL LESTE PAULI|CPFL MOCOCA|CPFL JAGUARI|CPFL SANTA CRUZ|CPFL SUL PAULIST|CPFL-PIRATINING|ELEKTRO|ELETROPAULO') then 'SP'
            when regexp_contains(distribuidora_raw, r'CELESC') then 'SC'
            when regexp_contains(distribuidora_raw, r'COPEL-DIS') then 'PR'
            when regexp_contains(distribuidora_raw, r'CEMIG-D') then 'MG'
            when regexp_contains(distribuidora_raw, r'LIGHT SESA') then 'RJ'
            when regexp_contains(distribuidora_raw, r'RGE SUL|RGE') then 'RS'
            when regexp_contains(distribuidora_raw, r'EMS') then 'MS'
            when regexp_contains(distribuidora_raw, r'EMT') then 'MT'
            when regexp_contains(distribuidora_raw, r'EPB') then 'PB'
            when regexp_contains(distribuidora_raw, r'ETO') then 'TO'
            else null
        end as uf,
        case
            when regexp_contains(distribuidora_raw, r'COELBA|COSERN|NEOENERGIA PE|CELPE|ENEL CE|EQUATORIAL AL|EQUATORIAL MA|EQUATORIAL PI|EPB') then 'Nordeste'
            when regexp_contains(distribuidora_raw, r'NEOENERGIA BRASILIA|EQUATORIAL GO') then 'Centro-Oeste'
            when regexp_contains(distribuidora_raw, r'ENEL RJ|LIGHT SESA|EDP ES|CEMIG-D') then 'Sudeste'
            when regexp_contains(distribuidora_raw, r'CPFL-|ELEKTRO|ELETROPAULO|EDP SP') then 'Sudeste'
            when regexp_contains(distribuidora_raw, r'CELESC|COPEL-DIS|RGE|RGE SUL') then 'Sul'
            when regexp_contains(distribuidora_raw, r'EQUATORIAL PA|ETO') then 'Norte'
            when regexp_contains(distribuidora_raw, r'EMS|EMT') then 'Centro-Oeste'
            else 'Nao informado'
        end as regiao,
        case
            when regexp_contains(distribuidora_raw, r'COELBA|COSERN|NEOENERGIA PE|CELPE|NEOENERGIA BRASILIA') then 'Neoenergia'
            when regexp_contains(distribuidora_raw, r'ENEL') then 'Enel'
            when regexp_contains(distribuidora_raw, r'EQUATORIAL') then 'Equatorial'
            when regexp_contains(distribuidora_raw, r'CPFL|ELEKTRO|RGE|RGE SUL') then 'CPFL Energia'
            when regexp_contains(distribuidora_raw, r'CEMIG') then 'Cemig'
            when regexp_contains(distribuidora_raw, r'COPEL') then 'Copel'
            when regexp_contains(distribuidora_raw, r'CELESC') then 'Celesc'
            when regexp_contains(distribuidora_raw, r'LIGHT') then 'Light'
            else 'Outros'
        end as grupo_economico,
        regexp_contains(distribuidora_raw, r'COELBA|NEOENERGIA COELBA|COMPANHIA DE ELETRICIDADE DO ESTADO DA BAHIA|CIA DE ELETRICIDADE DO ESTADO DA BAHIA') as flag_neoenergia_coelba
    from raw
),

pivoted as (
    select
        data_geracao_conjunto,
        distribuidora,
        sigla_distribuidora,
        cnpj_distribuidora,
        id_conjunto_unidades_consumidoras,
        descricao_conjunto_unidades_consumidoras,
        uf,
        regiao,
        grupo_economico,
        flag_neoenergia_coelba,
        ano,
        mes,
        data_referencia,
        max(case when sig_indicador = 'TMP' then valor_indicador end) as tmp,
        max(case when sig_indicador = 'TMD' then valor_indicador end) as tmd,
        max(case when sig_indicador = 'TME' then valor_indicador end) as tme,
        max(case when sig_indicador = 'TMM' then valor_indicador end) as tmae,
        max(case when sig_indicador = 'NUMOCORR' then valor_indicador end) as quantidade_ocorrencias,
        max(case when sig_indicador = 'NIE' then valor_indicador end) as quantidade_interrupcoes,
        max(case when sig_indicador = 'PNIE' then valor_indicador end) as percentual_interrupcoes,
        max(case when sig_indicador = 'NDIACRI' then valor_indicador end) as dias_criticos,
        max(case when sig_indicador = 'VLCLACRI' then valor_indicador end) as ocorrencias_em_dias_criticos
    from enriched
    group by all
),

final as (
    select
        *,
        coalesce(tmae, coalesce(tmp, 0) + coalesce(tmd, 0) + coalesce(tme, 0)) as tmae_recalculado,
        coalesce(
            quantidade_ocorrencias * coalesce(tmae, coalesce(tmp, 0) + coalesce(tmd, 0) + coalesce(tme, 0)),
            0
        ) as tempo_total_atendimento,
        case
            when coalesce(tmae, coalesce(tmp, 0) + coalesce(tmd, 0) + coalesce(tme, 0)) < 0 then true
            when coalesce(tmp, 0) < 0 or coalesce(tmd, 0) < 0 or coalesce(tme, 0) < 0 then true
            else false
        end as flag_registro_invalido
    from pivoted
)

select
    data_geracao_conjunto,
    distribuidora,
    sigla_distribuidora,
    cnpj_distribuidora,
    id_conjunto_unidades_consumidoras,
    descricao_conjunto_unidades_consumidoras,
    uf,
    regiao,
    grupo_economico,
    flag_neoenergia_coelba,
    ano,
    mes,
    data_referencia,
    tmp,
    tmd,
    tme,
    tmae_recalculado as tmae,
    quantidade_ocorrencias,
    quantidade_interrupcoes,
    percentual_interrupcoes,
    dias_criticos,
    ocorrencias_em_dias_criticos,
    tempo_total_atendimento,
    flag_registro_invalido
from final
where not flag_registro_invalido
