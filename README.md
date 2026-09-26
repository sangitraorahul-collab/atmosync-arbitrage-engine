# AtmoSync – Micro-Climate Arbitrage Analytics

## Project Overview

AtmoSync is an IoT analytics project that collects container telemetry data and transforms it into analytical data for monitoring and visualization.

## Project Architecture

Python IoT Simulator  
↓  
Apache Kafka  
↓  
MySQL  
↓  
dbt Core  
↓  
Power BI / Apache Superset

## dbt Models

### Staging Models

- `stg_iot_telemetry`
- `stg_commodity_prices`

### Analytical Models

- `fct_container_telemetry`
- `fct_telemetry_commodity`

## Week 2 – ELT Pipeline

Completed:

- dbt Core configuration
- dbt to MySQL connection
- IoT telemetry cleaning and standardization
- Data-quality tests
- Mock commodity pricing
- IoT and commodity pricing integration
- Final analytical model validation

## Week 3 – Cross-Support & Validation

Completed:

- dbt model validation
- NULL checks
- Duplicate ID checks
- Route and status validation
- Telemetry and commodity-price range validation
- Reusable SQL validation queries
- Preparation for dashboard integration

## Validation Results

| Metric | Result |
|---|---:|
| Final analytical records | 1,454 |
| Average temperature | 29.87 |
| Average humidity | 69.70 |
| Normal status | 747 |
| Warning status | 369 |
| At Risk status | 338 |

## Important Files

```text
dbt_project.yml
models/
├── staging/
│   ├── sources.yml
│   ├── staging.yml
│   ├── stg_iot_telemetry.sql
│   └── stg_commodity_prices.sql
└── marts/
    ├── marts.yml
    ├── fct_container_telemetry.sql
    └── fct_telemetry_commodity.sql

validation_queries.sql
WEEK2_PROGRESS.md
WEEK3_PROGRESS.md
