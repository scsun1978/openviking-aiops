# Network Monitoring Module

## Overview

This module provides network monitoring capabilities for the OpenViking AI Operations System.

## Features

- **Network Monitoring**
  - Ping latency monitoring
  - Bandwidth monitoring
  - Packet loss monitoring
  - Connection monitoring

- **Device Monitoring**
  - CPU usage monitoring
  - Memory usage monitoring
  - Disk usage monitoring

- **Alert Management**
  - Rule-based alerting
  - Multiple notification channels (Email, Webhook, Telegram)

- **Prometheus Metrics**
  - Expose metrics for Prometheus scraping
  - Configurable metrics port

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp config/.env.example config/.env
# Edit config/.env
```

## Running

```bash
# Run the service
python -m app.main
```

Prometheus metrics will be available at `http://localhost:9091/metrics`.

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## Docker

```bash
# Build image
docker build -t network-monitor .

# Run container
docker run -p 9091:9091 network-monitor
```
