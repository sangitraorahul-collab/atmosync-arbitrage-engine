WITH source_data AS (
    SELECT
        id,
        container_id,
        `timestamp`,
        temperature,
        humidity,
        vibration,
        route,
        status
    FROM {{ source('telemetry', 'raw_data') }}
),

cleaned AS (
    SELECT
        id,
        NULLIF(TRIM(container_id), '') AS container_id,
        `timestamp` AS telemetry_timestamp,
        CAST(temperature AS DECIMAL(10,2)) AS temperature,
        CAST(humidity AS DECIMAL(10,2)) AS humidity,
        CAST(vibration AS DECIMAL(10,2)) AS vibration,
        NULLIF(TRIM(route), '') AS route,
        LOWER(TRIM(status)) AS status
    FROM source_data
)

SELECT *
FROM cleaned