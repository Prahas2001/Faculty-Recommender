# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose ports for both FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Create a start script to run both servers
RUN echo '#!/bin/bash\nuvicorn Scraper.serving:app --host 0.0.0.0 --port 8000 & \nstreamlit run app.py --server.port 8501 --server.address 0.0.0.0' > start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]