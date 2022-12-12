{{ config(schema='prod') }}

SELECT 
    lastId - firstId + 1 as no_people,
    duration / (lastId - firstId + 1) as avg_duration,
    duration,
    {{ dbt.dateadd(datepart='second', interval='cast (a.duration * 1000 as integer)', from_date_or_timestamp="'2022-12-09'") }} as created_at
    
FROM `elite-bird-367213`.bq_ticketsim.wait_in_seller_line_1209 a