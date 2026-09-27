SELECT
    id,
    container_id,
    telemetry_timestamp,
    temperature,
    humidity,
    vibration,
    route,
    status,

    temperature_band,
    humidity_band,

    CASE
        WHEN temperature >= 35 AND humidity >= 80 THEN 'critical'
        WHEN temperature >= 35 OR humidity >= 80 THEN 'high'
        WHEN temperature >= 30 OR humidity >= 70 THEN 'medium'
        ELSE 'low'
    END AS spoilage_risk,

    CASE
        WHEN temperature >= 35 AND humidity >= 80 THEN 6
        WHEN temperature >= 35 OR humidity >= 80 THEN 12
        WHEN temperature >= 30 OR humidity >= 70 THEN 24
        ELSE 48
    END AS estimated_time_to_spoilage_hours,

    CASE
        WHEN temperature >= 35 AND humidity >= 80 THEN 'immediate action'
        WHEN temperature >= 35 OR humidity >= 80 THEN 'monitor closely'
        WHEN temperature >= 30 OR humidity >= 70 THEN 'monitor'
        ELSE 'normal'
    END AS recommended_action

FROM {{ ref('fct_container_telemetry') }}