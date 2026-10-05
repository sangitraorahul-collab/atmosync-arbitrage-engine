import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="telemetry_db",
    )


def main():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            alert_level,
            notification_status,
            COUNT(*) AS total
        FROM alert_activity
        GROUP BY alert_level, notification_status
        ORDER BY alert_level, notification_status
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    print("\nAtmoSync Alert Activity Report")
    print("=" * 40)

    if not rows:
        print("No alert activity recorded.")
    else:
        for row in rows:
            print(
                f"{row['alert_level']:10} | "
                f"{row['notification_status']:10} | "
                f"{row['total']}"
            )

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_alerts,
            SUM(slack_status = 'sent') AS slack_sent,
            SUM(email_status = 'sent') AS email_sent,
            SUM(notification_status = 'sent') AS fully_sent
        FROM alert_activity
        """
    )

    summary = cursor.fetchone()

    print("\nSummary")
    print("-" * 40)
    print(f"Total alerts: {summary['total_alerts']}")
    print(f"Slack sent: {summary['slack_sent']}")
    print(f"Email sent: {summary['email_sent']}")
    print(f"Fully delivered: {summary['fully_sent']}")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()