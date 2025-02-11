# Use official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies from existing requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the monitoring script
CMD ["python", "system_monitor.py"]
