{{ config(schema='prod') }}

SELECT 
    person as id,
    duration,
    {{ dbt.dateadd(datepart='minute', interval='cast (a.time as integer)', from_date_or_timestamp="'2022-12-09'") }} as created_at
    
FROM `elite-bird-367213`.bq_ticketsim.wait_in_scanner_line_1209 a