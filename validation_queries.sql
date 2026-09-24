USE telemetry_db;

-- 1. Final analytical model row count
SELECT COUNT(*) AS total_rows
FROM fct_telemetry_commodity;


-- 2. NULL validation
SELECT
    COUNT(*) AS total_rows,
    SUM(container_id IS NULL) AS null_container_id,
    SUM(route IS NULL) AS null_route,
    SUM(temperature IS NULL) AS null_temperature,
    SUM(humidity IS NULL) AS null_humidity,
    SUM(avg_commodity_price IS NULL) AS null_commodity_price,
    SUM(currency IS NULL) AS null_currency
FROM fct_telemetry_commodity;


-- 3. Duplicate ID validation
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT id) AS unique_ids,
    COUNT(*) - COUNT(DISTINCT id) AS duplicate_ids
FROM fct_telemetry_commodity;


-- 4. Show duplicate IDs if any exist
SELECT
    id,
    COUNT(*) AS duplicate_count
FROM fct_telemetry_commodity
GROUP BY id
HAVING COUNT(*) > 1;


-- 5. Validate status values
SELECT DISTINCT status
FROM fct_telemetry_commodity;


-- 6. Validate route values
SELECT DISTINCT route
FROM fct_telemetry_commodity;


-- 7. Validate telemetry measurement ranges
SELECT
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    MIN(humidity) AS min_humidity,
    MAX(humidity) AS max_humidity,
    MIN(vibration) AS min_vibration,
    MAX(vibration) AS max_vibration
FROM fct_telemetry_commodity;


-- 8. Validate commodity pricing range
SELECT
    MIN(avg_commodity_price) AS min_price,
    MAX(avg_commodity_price) AS max_price,
    COUNT(*) AS total_records
FROM fct_telemetry_commodity;


-- 9. Compare telemetry mart and final joined model
SELECT
    (SELECT COUNT(*) FROM fct_container_telemetry) AS telemetry_mart_rows,
    (SELECT COUNT(*) FROM fct_telemetry_commodity) AS final_model_rows;


-- 10. Check for missing commodity pricing
SELECT
    COUNT(*) AS records_without_commodity_price
FROM fct_telemetry_commodity
WHERE avg_commodity_price IS NULL;