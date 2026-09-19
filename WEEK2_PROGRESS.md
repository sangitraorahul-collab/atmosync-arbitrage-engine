\# AtmoSync – Week 2 Progress



\## Week 2: 12 September – 18 September 2026



\### Day 1 – dbt Core Configuration

\- Configured dbt Core 1.7.17.

\- Installed and configured the dbt MySQL adapter.

\- Connected dbt Core to the MySQL telemetry database.

\- Verified the database connection using `dbt debug`.



\### Day 2 – IoT Telemetry Staging

\- Created the `stg\_iot\_telemetry` staging model.

\- Cleaned and standardized raw IoT telemetry data.

\- Trimmed text fields and normalized container status.

\- Converted temperature, humidity, and vibration values to decimal types.

\- Renamed the raw timestamp field to `telemetry\_timestamp`.



\### Day 3 – Data Quality and Validation

\- Added dbt data-quality tests.

\- Added `not\_null` and `unique` tests for important fields.

\- Executed `dbt test`.

\- Validated the cleaned telemetry model.



\### Day 4 – Commodity Pricing Data

\- Created mock commodity pricing data.

\- Added commodity, route, timestamp, price, and currency fields.

\- Created the `stg\_commodity\_prices` staging model.

\- Standardized commodity, route, and currency values.

\- Converted commodity prices to decimal values.



\### Day 5 – IoT and Commodity Join

\- Created the `fct\_telemetry\_commodity` analytical model.

\- Joined cleaned IoT telemetry with route-level commodity pricing.

\- Used the latest available commodity pricing records.

\- Calculated route-level average commodity prices.



\### Day 6 – Final ELT Validation

\- Executed the dbt models successfully.

\- Validated the final analytical dataset.

\- Checked record counts and NULL values.

\- Confirmed that telemetry and commodity pricing were successfully combined.



\### Day 7 – Week 2 Completion

\- Completed the dbt ELT pipeline.

\- Verified the final analytical model.

\- Prepared the transformed dataset for Power BI and Apache Superset.

\- Documented the Week 2 implementation.



\## Week 2 Deliverables



\- dbt Core configuration

\- dbt to MySQL connection

\- IoT telemetry staging model

\- Commodity pricing staging model

\- Data-quality tests

\- Container telemetry analytical model

\- IoT and commodity pricing analytical model

\- Final ELT validation

\- Power BI / Superset-ready analytical dataset



\## Final Pipeline



Python IoT Simulator  

→ Apache Kafka  

→ MySQL  

→ dbt Core  

→ Staging Models  

→ Analytical Models  

→ Power BI / Apache Superset

