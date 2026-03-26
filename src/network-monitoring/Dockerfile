FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    iputils-ping \
    iproute2 \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Create logs directory
RUN mkdir -p logs

# Expose Prometheus metrics port
EXPOSE 9091

# Set environment variables
ENV PROMETHEUS_ENABLED=true
ENV PROMETHEUS_PORT=9091
ENV LOG_LEVEL=INFO

# Run the application
CMD ["python", "-m", "app.main"]
