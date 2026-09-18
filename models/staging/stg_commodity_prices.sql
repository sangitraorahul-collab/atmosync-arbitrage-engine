WITH source_data AS (

    SELECT
        price_id,
        commodity,
        route,
        price_timestamp,
        price_per_unit,
        currency
    FROM {{ source('telemetry', 'commodity_prices') }}

),

cleaned AS (

    SELECT
        price_id,
        TRIM(commodity) AS commodity,
        TRIM(route) AS route,
        price_timestamp,
        CAST(price_per_unit AS DECIMAL(10,2)) AS price_per_unit,
        UPPER(TRIM(currency)) AS currency
    FROM source_data

)

SELECT *
FROM cleaned