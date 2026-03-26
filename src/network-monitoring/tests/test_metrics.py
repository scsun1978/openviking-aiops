"""
Tests for metrics modules
"""

import pytest

from app.utils.config import PrometheusConfig


@pytest.fixture
def prometheus_config():
    """Create a test Prometheus configuration."""
    return PrometheusConfig(
        enabled=True,
        port=9091,
        path="/metrics"
    )


def test_metrics_collector_initialization(prometheus_config):
    """Test metrics collector initialization."""
    from app.metrics.metrics_collector import MetricsCollector
    
    collector = MetricsCollector(prometheus_config)
    
    assert collector is not None
    assert collector.config == prometheus_config


def test_prometheus_config_from_dict():
    """Test PrometheusConfig creation from dictionary."""
    data = {
        "enabled": True,
        "port": 9091,
        "path": "/metrics"
    }
    
    config = PrometheusConfig.from_dict(data)
    
    assert config.enabled is True
    assert config.port == 9091
    assert config.path == "/metrics"


def test_prometheus_config_defaults():
    """Test PrometheusConfig default values."""
    data = {}
    
    config = PrometheusConfig.from_dict(data)
    
    assert config.enabled is True  # Default enabled
    assert config.port == 9091  # Default port
    assert config.path == "/metrics"  # Default path
