# Use a more robust base image
FROM python:3.10

# Set working directory
WORKDIR /app

# --- IMPROVED: Install Chromium & Dependencies ---
# We added '--fix-missing' and changed the driver package name
RUN apt-get update --fix-missing && apt-get install -y \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables so Selenium knows where to look
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromium-driver

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Render uses port 10000 by default
EXPOSE 10000

# Run the FastAPI server
CMD ["sh", "-c", "uvicorn Scraper.serving:app --host 0.0.0.0 --port ${PORT:-10000}"]