\# AtmoSync – End-to-End Architecture



\## Overview



AtmoSync is a telemetry-driven logistics and arbitrage recommendation

system that transforms IoT telemetry and market data into actionable

recommendations and operational alerts.



\## End-to-End Flow



```text

IoT / Telemetry Data

&#x20;       ↓

MySQL

&#x20;       ↓

dbt ELT / Transformation

&#x20;       ↓

Recommendation Models

&#x20;       ↓

fct\_arbitrage\_recommendation

&#x20;       ↓

Python Alert Monitor

&#x20;       ↓

Alert Validation

&#x20;       ↓

Duplicate Detection

&#x20;       ↓

Slack / Email

&#x20;       ↓

alert\_activity

