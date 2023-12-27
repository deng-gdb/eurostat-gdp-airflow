{{ config(materialized='table') }}

with

regions as (

    select
        notation  as eu_commission_region_code,
        case
            when REGEXP_CONTAINS(notation,'^EL')
            then REGEXP_REPLACE(notation, '^EL', 'GR')
            when REGEXP_CONTAINS(notation,'^UK')
            then REGEXP_REPLACE(notation, '^UK', 'GB')
            else notation
        end       as region_code,
        label     as region_name

    from {{ ref('regions_lookup') }}

),


facts as (

    select 
        geo
    from {{ ref('casted_to_numeric_nama-10r-2gdp') }}

)

select    
    {{ dbt_utils.generate_surrogate_key(['region_code']) }} 
                 as region_id,
    regions.eu_commission_region_code,
    regions.region_code,
    regions.region_name
  from regions
 where exists (
    select geo
      from facts
     where facts.geo = regions.eu_commission_region_code
 )
