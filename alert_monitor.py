import os
import json
import smtplib
import urllib.request
import urllib.error

import mysql.connector
from email.message import EmailMessage


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
            telemetry_timestamp,
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


def validate_alert_row(row):
    required_fields = [
        "container_id",
        "route",
        "temperature",
        "humidity",
        "spoilage_risk",
        "reroute_required",
    ]

    for field in required_fields:
        if row.get(field) in (None, ""):
            return False

    try:
        float(row["temperature"])
        float(row["humidity"])
        int(row["reroute_required"])
    except (TypeError, ValueError):
        return False

    return True


def classify_alert(row):
    if not validate_alert_row(row):
        return "invalid"

    risk = str(row["spoilage_risk"]).strip().lower()
    reroute = int(row["reroute_required"])

    if risk == "critical":
        return "critical"

    if risk == "high" or reroute == 1:
        return "high"

    if risk == "medium":
        return "medium"

    if risk == "low":
        return "none"

    return "invalid"


def is_alert_candidate(row):
    return classify_alert(row) in ("critical", "high")


def build_alert_text(row):
    level = classify_alert(row)

    return (
        "🚨 *AtmoSync Alert*\n\n"
        f"*Alert Level:* {level.upper()}\n"
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
        f"{'YES' if int(row['reroute_required']) == 1 else 'NO'}"
    )


def send_slack_alert(row):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook_url:
        raise RuntimeError("SLACK_WEBHOOK_URL is not configured.")

    payload = json.dumps({
        "text": build_alert_text(row)
    }).encode("utf-8")

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


def build_email_body(row):
    level = classify_alert(row)

    return f"""AtmoSync Alert

Alert Level: {level.upper()}

Container: {row['container_id']}
Route: {row['route']}
Distance to Market: {row['distance_to_market_km']} km

Temperature: {row['temperature']} °C
Humidity: {row['humidity']} %
Vibration: {row['vibration']}

Spoilage Risk: {row['spoilage_risk'].upper()}
Estimated Time to Spoilage: {row['estimated_time_to_spoilage_hours']} hours
Recommended Action: {row['recommended_action']}
Routing Recommendation: {row['routing_recommendation']}
Arbitrage Priority: {row['arbitrage_priority'].upper()}
Reroute Required: {'YES' if int(row['reroute_required']) == 1 else 'NO'}
"""


def send_email_alert(row):
    smtp_host = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "465"))
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    sender = os.getenv("ALERT_EMAIL_FROM", username)
    recipient = os.getenv("ALERT_EMAIL_TO")

    if not username or not password or not recipient:
        raise RuntimeError("Email configuration is missing.")

    message = EmailMessage()
    message["Subject"] = (
        f"[AtmoSync {classify_alert(row).upper()}] "
        f"Container {row['container_id']}"
    )
    message["From"] = sender
    message["To"] = recipient
    message.set_content(build_email_body(row))

    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20) as server:
        server.login(username, password)
        server.send_message(message)

    return "Email sent successfully"


def main():
    connection = None

    try:
        connection = get_connection()
        rows = get_alert_candidates(connection)

        print(f"Found {len(rows)} alert candidates.")

        if not rows:
            print("No alert candidates found.")
            return

        row = rows[0]

        if not is_alert_candidate(row):
            print("Selected record is not a valid alert candidate.")
            return

        print(f"Testing alert for container: {row['container_id']}")

        print("Sending Slack alert...")
        print(f"Slack response: {send_slack_alert(row)}")

        print("Sending email alert...")
        print(send_email_alert(row))

    except mysql.connector.Error as exc:
        print(f"MySQL error: {exc}")
    except Exception as exc:
        print(f"Alert monitor error: {exc}")
    finally:
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()