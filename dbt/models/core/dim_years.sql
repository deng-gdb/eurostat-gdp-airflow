{{ config(materialized='table') }}

select {{ dbt_utils.generate_surrogate_key(['year']) }} as year_id,
       year
  from {{ ref('selected_distint_years') }}
 order by 2 desc