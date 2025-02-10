# System_monitor
A basic system metric logger I created for my friend's PC that always crashes (smh)
Also sends out an alert email to me before it crashes so i can scream at them to close the 100 open Chrome Tabs 

## 📌 Features
- Detects high CPU, RAM, and Disk usage.
- Sends an email **before** or **after** a system crash.
- Uses `.env` for storing credentials securely.
- Prevents repeated email alerts.

## 🚀 Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

 2. Edit .env File
    Input your email addresses so the email alerts can be sent.

  3. Run the Script
     
