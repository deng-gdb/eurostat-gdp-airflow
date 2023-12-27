{{ config(materialized='view') }}

select distinct year
  from {{ ref('casted_to_numeric_nama-10r-2gdp') }}
