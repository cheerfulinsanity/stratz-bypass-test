# Use official Python image
FROM python:3.11-slim

# Install system dependencies for Chromium
RUN apt-get update && apt-get install -y \
    curl wget unzip \
    libglib2.0-0 libnss3 libatk-bridge2.0-0 libx11-xcb1 \
    libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 \
    libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 \
    libxshmfence1 libgtk-3-0 fonts-liberation libappindicator3-1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright browser binaries
RUN python -m playwright install chromium

# Copy source code
COPY . /app
WORKDIR /app

# Run the script on startup
CMD ["python", "stratz_test.py"]

