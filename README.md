# System Monitor 🚀  

I created a basic system metric logger for my girlfriend's PC that always crashes (smh). It sends out an alert email before it crashes so I can scream at them to close the 100 open Chrome tabs.  

## 📌 Features  
✅ Detects high CPU, RAM, and Disk usage.  
✅ Sends an email before or after a system crash.  
✅ Uses `.env` for storing credentials securely.  
✅ Prevents repeated email alerts.  
✅ **Now supports Docker for easier deployment!**  

## 🚀 Setup Instructions  

### 1️⃣ Install Dependencies  
```sh
pip install -r requirements.txt
```

### 2️⃣ Configure Environment Variables

Create a .env file and add your email credentials:

```ini
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_password
```

### 3️⃣ Run the Script

```sh
python monitor.py
```

## 🐳 Running with Docker (Optional)

If you prefer using Docker, follow these steps:

### 1️⃣ Build the Docker Image

```sh
docker build -t system_monitor .
```

### 2️⃣ Run the Container

```sh
docker run --env-file .env system_monitor
```

Now the system monitor will run inside a Docker container! 🎉
