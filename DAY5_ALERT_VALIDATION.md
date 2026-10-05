\# Week 4 – Day 5 Alert Validation



\## Objective



Implement alert activity logging and duplicate-alert prevention.



\## Alert Activity Table



Created `alert\_activity` with:



\- source\_record\_id

\- container\_id

\- alert\_level

\- alert\_timestamp

\- slack\_status

\- email\_status

\- notification\_status



A unique constraint was added on:



\- source\_record\_id

\- alert\_level



\## First Execution



Container: C005  

Alert level: high



Result:

\- Slack notification: sent

\- Alert activity: recorded

\- Notification status: sent



Email was disabled during the duplicate-prevention test.



\## Second Execution



The same C005 high-level alert was processed again.



Expected:

\- Existing alert detected

\- Slack notification skipped

\- No duplicate alert record created



\## Validation



\- Alert logging: PASS

\- Duplicate prevention: PASS

\- Unique constraint: PASS

\- Slack notification tracking: PASS

