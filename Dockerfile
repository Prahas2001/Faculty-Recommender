# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# --- CRITICAL: Install Chrome & System Dependencies ---
# These are required for Selenium to run on a Linux server
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Render provides the port via $PORT, default to 10000
EXPOSE 10000

# Run ONLY the FastAPI server
# Using ${PORT:-10000} ensures it works both locally and on Render
CMD ["sh", "-c", "uvicorn Scraper.serving:app --host 0.0.0.0 --port ${PORT:-10000}"]