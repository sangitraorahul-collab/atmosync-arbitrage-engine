\# AtmoSync – Week 4 Alerting Module



\## Overview



The Week 4 alerting module detects high-risk recommendations from

`fct\_arbitrage\_recommendation` and delivers notifications through Slack

and email.



\## Alert Flow



MySQL

→ dbt recommendation model

→ Python alert monitor

→ Alert validation

→ Duplicate check

→ Slack / Email

→ Alert activity logging



\## Implemented Features



\- Alert candidate detection

\- Critical and high-risk classification

\- Invalid-data validation

\- Slack notifications

\- Email notifications

\- Alert activity logging

\- Duplicate-alert prevention

\- Notification status tracking



\## Alert Activity



The `alert\_activity` table records:



\- Source record ID

\- Container ID

\- Alert level

\- Alert timestamp

\- Slack status

\- Email status

\- Notification status



\## Validation



Slack notification:

PASS



Email notification:

PASS



Alert rule tests:

4/4 PASS



Duplicate prevention:

PASS



\## Security



Credentials and webhook URLs are stored using environment variables

and are not hard-coded in the source code.

