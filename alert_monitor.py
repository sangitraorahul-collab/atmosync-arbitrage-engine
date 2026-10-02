import os
import json
import urllib.request
import urllib.error
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="telemetry_db",
    )


def get_alert_candidates(connection):
    query = """
        SELECT
            id,
            container_id,
            route,
            temperature,
            humidity,
            vibration,
            distance_to_market_km,
            spoilage_risk,
            estimated_time_to_spoilage_hours,
            recommended_action,
            routing_recommendation,
            arbitrage_priority,
            reroute_required
        FROM fct_arbitrage_recommendation
        WHERE reroute_required = 1
           OR spoilage_risk IN ('critical', 'high')
        ORDER BY telemetry_timestamp DESC
    """

    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def send_slack_alert(row):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        raise RuntimeError("SLACK_WEBHOOK_URL is not configured.")

    message = (
        "🚨 *AtmoSync Alert*\n\n"
        f"*Container:* {row['container_id']}\n"
        f"*Route:* {row['route']}\n"
        f"*Distance to Market:* {row['distance_to_market_km']} km\n\n"
        f"*Temperature:* {row['temperature']}°C\n"
        f"*Humidity:* {row['humidity']}%\n"
        f"*Vibration:* {row['vibration']}\n\n"
        f"*Spoilage Risk:* {row['spoilage_risk'].upper()}\n"
        f"*Estimated Time to Spoilage:* "
        f"{row['estimated_time_to_spoilage_hours']} hours\n"
        f"*Recommended Action:* {row['recommended_action']}\n"
        f"*Routing Recommendation:* {row['routing_recommendation']}\n"
        f"*Arbitrage Priority:* {row['arbitrage_priority'].upper()}\n"
        f"*Reroute Required:* "
        f"{'YES' if row['reroute_required'] == 1 else 'NO'}"
    )

    payload = json.dumps({"text": message}).encode("utf-8")

    request = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Slack request failed: {exc}") from exc


def main():
    connection = None

    try:
        connection = get_connection()
        rows = get_alert_candidates(connection)

        print(f"Found {len(rows)} alert candidates.")

        # Day 2: send only one alert as a safe integration test.
        if rows:
            row = rows[0]
            print(f"Testing alert for container: {row['container_id']}")
            result = send_slack_alert(row)
            print(f"Slack response: {result}")
        else:
            print("No alert candidates found.")

    except mysql.connector.Error as exc:
        print(f"MySQL error: {exc}")
    except Exception as exc:
        print(f"Alert monitor error: {exc}")
    finally:
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()