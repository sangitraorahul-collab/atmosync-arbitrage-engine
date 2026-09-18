WITH latest_prices AS (

    SELECT
        commodity,
        route,
        price_timestamp,
        price_per_unit,
        currency,
        ROW_NUMBER() OVER (
            PARTITION BY commodity, route
            ORDER BY price_timestamp DESC
        ) AS rn
    FROM {{ ref('stg_commodity_prices') }}

),

route_prices AS (

    SELECT
        route,
        ROUND(AVG(price_per_unit), 2) AS avg_commodity_price,
        MAX(price_timestamp) AS price_timestamp,
        currency
    FROM latest_prices
    WHERE rn = 1
    GROUP BY
        route,
        currency

)

SELECT
    t.id,
    t.container_id,
    t.telemetry_timestamp,
    t.temperature,
    t.humidity,
    t.vibration,
    t.route,
    t.status,
    t.temperature_band,
    t.humidity_band,
    p.avg_commodity_price,
    p.price_timestamp,
    p.currency

FROM {{ ref('fct_container_telemetry') }} AS t

LEFT JOIN route_prices AS p
    ON t.route = p.route