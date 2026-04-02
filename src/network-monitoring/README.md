# Network Monitoring Service

AI-based network monitoring and alerting system for edge computing environments.

## Features

### Network Monitoring
- **Network Latency**: ICMP ping monitoring with histogram metrics
- **Network Bandwidth**: Traffic monitoring with bytes and rate tracking
- **Packet Loss**: Packet loss ratio calculation
- **Connection Monitoring**: TCP connection state tracking
- **Port Monitoring**: Port status checking

### Device Monitoring
- **CPU Usage**: Usage, cores count, and frequency monitoring
- **Memory Usage**: Usage, total, and available memory monitoring
- **Disk Usage**: Usage, total, used, and free space monitoring
- **Temperature**: Temperature sensor monitoring
- **Power Status**: Battery/power-plugged status detection
- **Uptime**: System uptime tracking

### Alerting
- **Rule Engine**: YAML/JSON-based alert rules
- **Threshold Detection**: Support for >, <, =, !=, >=, <= operators
- **Trend Detection**: Growth and decline rate monitoring
- **Rule Aggregation**: AND/OR logic for multiple conditions
- **Alert Suppression**: Configurable suppression duration
- **Alert History**: Full alert history tracking

### Notifications
- **Email**: SMTP-based email notifications
- **Webhook**: HTTP webhook notifications
- **Telegram**: Telegram bot notifications with rich formatting

## Installation

### Prerequisites
- Python 3.10+
- Docker (optional)

### From Source

```bash
# Clone repository
git clone https://github.com/scsun1978/openviking-aiops.git
cd openviking-aiops/src/network-monitoring

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp config/config.yaml.example config/config.yaml
# Edit config/config.yaml with your settings

# Run
python app/main.py config/config.yaml
```

### Using Docker

```bash
# Build image
docker build -t network-monitoring .

# Run container
docker run -d \
  -p 9090:9090 \
  -v $(pwd)/config:/app/config \
  network-monitoring
```

## Configuration

### Configuration File Structure

```yaml
# monitoring/config/config.yaml

monitoring:
  # Monitoring targets
  targets:
    - host: "127.0.0.1"
      port: 22
      name: "localhost"

  # Monitoring intervals (seconds)
  intervals:
    ping: 60
    bandwidth: 10
    cpu: 10
    memory: 10
    disk: 60

  # Prometheus configuration
  prometheus:
    enabled: true
    host: "0.0.0.0"
    port: 9090

alerts:
  enabled: true
  evaluation_interval: 60  # seconds
  rules_file: "config/alert-rules.yaml"

notifications:
  email:
    enabled: false
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    smtp_username: "your-email@gmail.com"
    smtp_password: "your-password"
    from_address: "noreply@example.com"
    to_address: "alerts@example.com"

  webhook:
    enabled: false
    url: "https://example.com/webhook"
    timeout: 10

  telegram:
    enabled: false
    bot_token: "your-bot-token"
    chat_id: "123456789"
```

### Alert Rules Configuration

```yaml
# config/alert-rules.yaml

rules:
  - name: cpu_high_usage
    enabled: true
    severity: critical
    message: "CPU usage is too high"
    labels:
      service: "system"
    aggregator: AND
    suppress_duration: 300  # 5 minutes
    conditions:
      - metric: "cpu_usage_ratio"
        operator: ">"
        threshold: 0.8  # 80%
        duration: 60  # 1 minute
```

## Metrics

### Network Metrics
- `network_ping_latency_ms` - Ping latency histogram
- `network_ping_success_total` - Successful pings counter
- `network_ping_failure_total` - Failed pings counter
- `network_packet_loss_ratio` - Packet loss ratio
- `network_bandwidth_bytes` - Network traffic bytes
- `network_bandwidth_bytes_per_sec` - Network traffic rate
- `network_connections_count` - TCP connection count
- `network_port_status` - Port status

### Device Metrics
- `cpu_usage_ratio` - CPU usage ratio
- `cpu_cores_count` - CPU cores count
- `cpu_frequency_mhz` - CPU frequency
- `memory_usage_ratio` - Memory usage ratio
- `memory_total_bytes` - Total memory bytes
- `memory_available_bytes` - Available memory bytes
- `disk_usage_ratio` - Disk usage ratio
- `disk_total_bytes` - Total disk bytes
- `disk_used_bytes` - Used disk bytes
- `disk_free_bytes` - Free disk bytes
- `device_temperature_celsius` - Device temperature
- `device_power_status` - Power status
- `device_uptime_seconds` - System uptime

## Usage

### Start Monitoring Service

```bash
# Start with default configuration
python app/main.py

# Start with custom configuration
python app/main.py /path/to/config.yaml
```

### Prometheus Integration

Configure Prometheus to scrape metrics:

```yaml
scrape_configs:
  - job_name: 'network-monitoring'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:9090']
```

### Grafana Dashboard

Import the provided dashboard JSON to visualize metrics.

## Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_monitors.py -v
```

### Test Coverage

Current coverage: ~70%

- `tests/test_monitors.py` - Configuration tests
- `tests/test_alerts.py` - Configuration tests
- `tests/test_metrics.py` - Configuration tests
- `tests/test_rule_engine.py` - Rule parsing and evaluation tests
- `tests/test_notifiers.py` - Notification tests

## Architecture

```
┌─────────────────────────────────────────────────────┐
│           Network Monitoring Service                │
├─────────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────────┐  ┌──────────────┐               │
│  │ Network       │  │ Device        │               │
│  │ Monitor       │  │ Monitor       │               │
│  │               │  │               │               │
│  │ • Ping        │  │ • CPU         │               │
│  │ • Bandwidth   │  │ • Memory      │               │
│  │ • Connections │  │ • Disk        │               │
│  │ • Ports       │  │ • Temperature │               │
│  └──────┬───────┘  └──────┬───────┘               │
│         │                     │                         │
│         └──────────┬──────────┘                         │
│                    │                                    │
│         ┌──────────▼──────────┐                         │
│         │  Metrics          │                         │
│         │  Collector        │                         │
│         └──────────┬──────────┘                         │
│                    │                                    │
│         ┌──────────▼──────────┐                         │
│         │  Alert Manager    │                         │
│         │                   │                         │
│  ┌──────▼────────┬────────▼──────┐               │
│  │  Rule        │  Notifications│               │
│  │  Evaluator    │               │
│  │              │  ┌──────────┬──▼──────┐         │
│  │              │  │ Email    │Webhook  │         │
│  └──────┬───────┘  └──────────┬───────┘         │
│         │                     │                      │
│  ┌──────▼─────────────────────▼──────┐            │
│  │      Prometheus Metrics Server    │            │
│  │           :9090                     │            │
│  └───────────────────────────────────────┘            │
└─────────────────────────────────────────────────────┘
```

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues and questions, please open an issue on GitHub.
