SELECT
    id,
    container_id,
    telemetry_timestamp,
    route,

    temperature,
    humidity,
    vibration,
    status,

    distance_to_market_km,

    spoilage_risk,
    estimated_time_to_spoilage_hours,
    recommended_action,

    CASE
        WHEN spoilage_risk = 'critical' THEN 'urgent reroute'
        WHEN spoilage_risk = 'high' THEN 'reroute recommended'
        WHEN spoilage_risk = 'medium' THEN 'monitor route'
        ELSE 'continue current route'
    END AS routing_recommendation,

    CASE
        WHEN spoilage_risk = 'critical' THEN 'urgent'
        WHEN spoilage_risk = 'high' THEN 'high'
        WHEN spoilage_risk = 'medium' THEN 'medium'
        ELSE 'low'
    END AS arbitrage_priority,

    CASE
        WHEN spoilage_risk IN ('critical', 'high')
            THEN 1
        ELSE 0
    END AS reroute_required

FROM {{ ref('fct_distance_to_market') }}