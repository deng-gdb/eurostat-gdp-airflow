{{ config(materialized='view') }}


select trim(string_field_0)  as unit,
       trim(string_field_1)  as geo,
       trim(string_field_2)  as `2021`,
       trim(string_field_3)  as `2020`,
       trim(string_field_4)  as `2019`,
       trim(string_field_5)  as `2018`,
       trim(cast(double_field_6 as string)) as `2017`,
       trim(string_field_7)  as `2016`,
       trim(string_field_8)  as `2015`,
       trim(cast(double_field_9 as string)) as `2014`,
       trim(string_field_10) as `2013`,
       trim(string_field_11) as `2012`,
       trim(string_field_12) as `2011`,
       trim(string_field_13) as `2010`,
       trim(string_field_14) as `2009`,
       trim(string_field_15) as `2008`,
       trim(cast(string_field_16 as string)) as `2007`,
       trim(string_field_17) as `2006`,
       trim(string_field_18) as `2005`,
       trim(cast(string_field_19 as string)) as `2004`,
       trim(string_field_20) as `2003`,
       trim(string_field_21) as `2002`,
       trim(string_field_22) as `2001`,
       trim(string_field_23) as `2000`
  from {{ source('staging','nama-10r-2gdp') }}