{{ config(
       materialized='table',
       partition_by={
           "field": "year",
           "data_type": "int64",
           "range": {
                "start": 2000,
                "end": 3000,
                "interval": 1
            }
       },
       cluster_by = ["region_name", "unit_name"]   
   ) 
}}


with

regions as (

    select
        region_id,
        region_code,
        eu_commission_region_code,
        region_name

    from {{ ref('dim_regions') }}

),

units as (

    select
        unit_id,
        unit_code,
        unit_name

    from {{ ref('dim_units') }}

),

years as (

    select
        year_id,
        year

    from {{ ref('dim_years') }}

),

facts as (

    select 
        unit,
        geo,
        year,
        value
    from {{ ref('casted_to_numeric_nama-10r-2gdp') }}

)

select    
    units.unit_name,
    regions.region_name,
    regions.region_code,
    years.year,
    facts.value
  from facts
      inner join years
         on facts.year = years.year
      inner join units 
         on units.unit_code = facts.unit
      inner join regions  
         on regions.eu_commission_region_code = facts.geo