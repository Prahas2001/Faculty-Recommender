FROM python:3.10-slim

WORKDIR /app

# Install only necessary system libs
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Prevent python from writing bytecode
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Critical: Use the $PORT variable Render provides
CMD ["sh", "-c", "uvicorn Scraper.serving:app --host 0.0.0.0 --port ${PORT:-10000} --workers 1"]
