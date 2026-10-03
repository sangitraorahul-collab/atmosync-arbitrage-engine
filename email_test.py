import os
import smtplib
from email.message import EmailMessage


smtp_host = "smtp.gmail.com"
smtp_port = 465

username = os.getenv("EMAIL_USERNAME")
password = os.getenv("EMAIL_PASSWORD")
sender = os.getenv("ALERT_EMAIL_FROM", username)
recipient = os.getenv("ALERT_EMAIL_TO")

if not username:
    raise RuntimeError("EMAIL_USERNAME is missing.")

if not password:
    raise RuntimeError("EMAIL_PASSWORD is missing.")

if not recipient:
    raise RuntimeError("ALERT_EMAIL_TO is missing.")


message = EmailMessage()
message["Subject"] = "[AtmoSync TEST] Email alert working"
message["From"] = sender
message["To"] = recipient

message.set_content(
    """AtmoSync Email Test

This is a test notification for the Week 4 Day 3 alert module.

Email notification is working successfully.
"""
)


with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20) as server:
    server.login(username, password)
    server.send_message(message)


print("Email sent successfully.")