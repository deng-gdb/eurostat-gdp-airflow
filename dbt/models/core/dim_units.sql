{{ config(materialized='table') }}

with

units as (

    select
        id    as unit_code,
        label as unit_name

    from {{ ref('units_lookup') }}

),


facts as (

    select 
        unit
    from {{ ref('casted_to_numeric_nama-10r-2gdp') }}

)

select    
    {{ dbt_utils.generate_surrogate_key(['unit_code']) }} 
                 as unit_id,
    units.unit_code,
    units.unit_name
  from units
 where exists (
    select unit
      from facts
     where facts.unit = units.unit_code
 )