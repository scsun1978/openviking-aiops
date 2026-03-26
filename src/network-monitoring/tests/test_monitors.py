"""
Tests for monitor modules
"""

import pytest

from app.utils.config import MonitoringConfig, MonitoringTarget


@pytest.fixture
def monitoring_config():
    """Create a test monitoring configuration."""
    return MonitoringConfig(
        targets=[
            MonitoringTarget(host="127.0.0.1", port=22, name="localhost"),
        ],
        intervals={
            "ping": 60,
            "bandwidth": 10,
            "cpu": 10,
            "memory": 10,
            "disk": 60,
        }
    )


def test_monitoring_config_initialization():
    """Test monitoring configuration creation."""
    target = MonitoringTarget(
        host="127.0.0.1",
        port=22,
        name="localhost"
    )
    
    assert target.host == "127.0.0.1"
    assert target.port == 22
    assert target.name == "localhost"


def test_monitoring_config_from_dict():
    """Test MonitoringConfig creation from dictionary."""
    data = {
        "targets": [
            {"host": "127.0.0.1", "port": 22, "name": "localhost"}
        ],
        "intervals": {
            "ping": 60,
            "bandwidth": 10,
            "cpu": 10,
            "memory": 10,
            "disk": 60,
        }
    }
    
    config = MonitoringConfig.from_dict(data)
    
    assert len(config.targets) == 1
    assert config.targets[0].host == "127.0.0.1"
    assert config.intervals["ping"] == 60


def test_monitoring_config_defaults():
    """Test MonitoringConfig default values."""
    data = {"targets": []}
    
    config = MonitoringConfig.from_dict(data)
    
    assert config.targets == []
    assert "ping" in config.intervals
    assert "cpu" in config.intervals
