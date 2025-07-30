# Minimal base image with Python
FROM python:3.11-slim

# Install system packages needed for pip and networking
RUN apt-get update && apt-get install -y \
    curl gcc libffi-dev libssl-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app
WORKDIR /app

# Run the script at container start
CMD ["python", "stratz_test.py"]
