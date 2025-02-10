import psutil
import smtplib
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

ALERT_THRESHOLD_CPU = 90  # CPU usage threshold %
ALERT_THRESHOLD_RAM = 90  # RAM usage threshold %
ALERT_THRESHOLD_TEMP = 85  # CPU temperature threshold (if supported)
CHECK_INTERVAL = 5  # Seconds between checks

def get_chrome_memory_usage():
    """Returns total memory usage of all Chrome processes."""
    total_memory = 0
    for process in psutil.process_iter(attrs=['name', 'memory_info']):
        if process.info['name'] and "chrome" in process.info['name'].lower():
            total_memory += process.info['memory_info'].rss  # Resident Set Size (RAM)
    return total_memory / (1024 * 1024)  # Convert to MB

def get_cpu_temperature():
    """Returns CPU temperature if available, otherwise None."""
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            return temps["coretemp"][0].current  # Return first core's temperature
    return None  # If temperature data is not available

def send_email_alert(subject, body):
    """Sends an email alert."""
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message)
        print("[ALERT] Email sent successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def monitor_system():
    """Monitors CPU, RAM, Chrome memory usage, and temperature."""
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        chrome_memory = get_chrome_memory_usage()
        cpu_temp = get_cpu_temperature()

        print(f"CPU: {cpu_usage}%, RAM: {ram_usage}%, Chrome Memory: {chrome_memory:.2f} MB")
        if cpu_temp:
            print(f"CPU Temperature: {cpu_temp}°C")

        # Alert conditions
        if cpu_usage > ALERT_THRESHOLD_CPU or ram_usage > ALERT_THRESHOLD_RAM or (cpu_temp and cpu_temp > ALERT_THRESHOLD_TEMP):
            alert_msg = f"High Resource Usage Detected!\nCPU: {cpu_usage}%\nRAM: {ram_usage}%\nChrome Memory: {chrome_memory:.2f} MB"
            if cpu_temp:
                alert_msg += f"\nCPU Temp: {cpu_temp}°C"
            send_email_alert("🚨 System Warning: High Usage Detected!", alert_msg)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_system()
