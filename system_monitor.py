import psutil
import time
import os
import datetime
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

# Configuration
LOG_INTERVAL = 10  # Time interval in seconds
CRASH_THRESHOLD = {"CPU": 95, "RAM": 95, "Disk": 95}  # Threshold for critical usage

def send_email(subject, message):
    """Sends an email notification."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print(f"📧 Email sent: {subject}")
    except Exception as e:
        print(f"⚠️ Failed to send email: {e}")

def log_and_check_crash():
    """Logs system metrics and sends an email before a crash occurs."""
    last_known_state = None
    crash_warning_sent = False

    while True:
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent

            log_data = {
                "Timestamp": timestamp,
                "CPU Usage (%)": cpu_usage,
                "RAM Usage (%)": ram_usage,
                "Disk Usage (%)": disk_usage
            }

            last_known_state = log_data  # Save last known state

            print(f"[{timestamp}] CPU: {cpu_usage}%, RAM: {ram_usage}%, Disk: {disk_usage}%")

            # If any metric exceeds the crash threshold, send a warning email
            if (cpu_usage > CRASH_THRESHOLD["CPU"] or
                ram_usage > CRASH_THRESHOLD["RAM"] or
                disk_usage > CRASH_THRESHOLD["Disk"]):

                if not crash_warning_sent:  # Avoid sending multiple alerts
                    send_email("⚠️ Warning: System May Crash!", f"High resource usage detected:\n{json.dumps(log_data, indent=2)}")
                    crash_warning_sent = True

            else:
                crash_warning_sent = False  # Reset warning flag if system stabilizes

            time.sleep(LOG_INTERVAL)

        except Exception as e:
            print(f"⚠️ System crashed or monitoring failed: {e}")
            if last_known_state:
                send_email("🚨 System Crashed!", f"Last known state before crash:\n{json.dumps(last_known_state, indent=2)}")
            break

if __name__ == "__main__":
    print("🚀 Monitoring system for potential crashes... Press Ctrl+C to stop.")
    try:
        log_and_check_crash()
    except KeyboardInterrupt:
        print("🛑 Monitoring stopped.")
