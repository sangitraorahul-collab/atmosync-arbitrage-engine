SELECT
    id,
    container_id,
    telemetry_timestamp,
    route,
    temperature,
    humidity,
    vibration,
    status,
    spoilage_risk,
    estimated_time_to_spoilage_hours,
    recommended_action,

    CASE
        WHEN route = 'Pune-Mumbai' THEN 150
        WHEN route = 'Nashik-Pune' THEN 210
        WHEN route = 'Pune-Nagpur' THEN 720
        WHEN route = 'Mumbai-Nashik' THEN 165
        ELSE NULL
    END AS distance_to_market_km

FROM {{ ref('fct_spoilage_risk') }}