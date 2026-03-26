"""
Tests for alert modules
"""

import pytest

from app.utils.config import AlertsConfig, NotificationConfig


def test_alerts_config_initialization():
    """Test alerts configuration creation."""
    config = AlertsConfig(
        enabled=True,
        rules_file="config/alert_rules.yaml"
    )
    
    assert config.enabled is True
    assert config.rules_file == "config/alert_rules.yaml"


def test_alerts_config_from_dict():
    """Test AlertsConfig creation from dictionary."""
    data = {
        "enabled": True,
        "rules_file": "config/alert_rules.yaml"
    }
    
    config = AlertsConfig.from_dict(data)
    
    assert config.enabled is True
    assert config.rules_file == "config/alert_rules.yaml"


def test_notification_config_initialization():
    """Test notification configuration creation."""
    config = NotificationConfig(
        email={
            "enabled": False,
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587
        },
        webhook={
            "enabled": False,
            "url": "https://hooks.slack.com/services/..."
        },
        telegram={
            "enabled": False,
            "bot_token": "TEST_TOKEN",
            "chat_id": "123456789"
        }
    )
    
    assert config.email["enabled"] is False
    assert config.webhook["url"] == "https://hooks.slack.com/services/..."
    assert config.telegram["bot_token"] == "TEST_TOKEN"


def test_notification_config_from_dict():
    """Test NotificationConfig creation from dictionary."""
    data = {
        "email": {"enabled": False},
        "webhook": {"enabled": False},
        "telegram": {"enabled": False}
    }
    
    config = NotificationConfig.from_dict(data)
    
    assert config.email["enabled"] is False
    assert config.webhook["enabled"] is False
    assert config.telegram["enabled"] is False
