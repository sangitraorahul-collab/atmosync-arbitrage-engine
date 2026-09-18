SELECT
    id,
    container_id,
    telemetry_timestamp,
    temperature,
    humidity,
    vibration,
    route,
    status,

    CASE
        WHEN temperature >= 35 THEN 'high'
        WHEN temperature <= 5 THEN 'low'
        ELSE 'normal'
    END AS temperature_band,

    CASE
        WHEN humidity >= 80 THEN 'high'
        WHEN humidity <= 30 THEN 'low'
        ELSE 'normal'
    END AS humidity_band

FROM {{ ref('stg_iot_telemetry') }}