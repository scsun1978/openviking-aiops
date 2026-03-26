"""
Configuration management module
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class PrometheusConfig:
    """Prometheus configuration."""

    enabled: bool = True
    port: int = 9091
    path: str = "/metrics"

    @classmethod
    def from_dict(cls, data: dict) -> "PrometheusConfig":
        """Create PrometheusConfig from dictionary."""
        return cls(
            enabled=data.get("enabled", True),
            port=data.get("port", 9091),
            path=data.get("path", "/metrics"),
        )


@dataclass
class MonitoringTarget:
    """Monitoring target configuration."""

    host: str
    port: int
    name: str


@dataclass
class MonitoringConfig:
    """Monitoring configuration."""

    targets: List[MonitoringTarget]
    intervals: dict

    @classmethod
    def from_dict(cls, data: dict) -> "MonitoringConfig":
        """Create MonitoringConfig from dictionary."""
        targets = [
            MonitoringTarget(host=t["host"], port=t["port"], name=t["name"])
            for t in data.get("targets", [])
        ]
        return cls(
            targets=targets,
            intervals=data.get("intervals", {
                "ping": 60,
                "bandwidth": 10,
                "cpu": 10,
                "memory": 10,
                "disk": 60,
            }),
        )


@dataclass
class AlertsConfig:
    """Alerts configuration."""

    enabled: bool = True
    rules_file: str = "config/alert_rules.yaml"

    @classmethod
    def from_dict(cls, data: dict) -> "AlertsConfig":
        """Create AlertsConfig from dictionary."""
        return cls(
            enabled=data.get("enabled", True),
            rules_file=data.get("rules_file", "config/alert_rules.yaml"),
        )


@dataclass
class NotificationConfig:
    """Notification configuration."""

    email: dict
    webhook: dict
    telegram: dict

    @classmethod
    def from_dict(cls, data: dict) -> "NotificationConfig":
        """Create NotificationConfig from dictionary."""
        return cls(
            email=data.get("email", {"enabled": False}),
            webhook=data.get("webhook", {"enabled": False}),
            telegram=data.get("telegram", {"enabled": False}),
        )


@dataclass
class LoggingConfig:
    """Logging configuration."""

    level: str = "INFO"
    file: str = "logs/network-monitor.log"
    max_bytes: int = 10485760
    backup_count: int = 5

    @classmethod
    def from_dict(cls, data: dict) -> "LoggingConfig":
        """Create LoggingConfig from dictionary."""
        return cls(
            level=data.get("level", "INFO"),
            file=data.get("file", "logs/network-monitor.log"),
            max_bytes=data.get("max_bytes", 10485760),
            backup_count=data.get("backup_count", 5),
        )


@dataclass
class Config:
    """Main configuration class."""

    monitoring: MonitoringConfig
    prometheus: PrometheusConfig
    alerts: AlertsConfig
    notifications: NotificationConfig
    logging: LoggingConfig

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        """Load configuration from YAML file."""
        if config_path is None:
            # Default config path
            config_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..",
                "config",
                "config.yaml"
            )

        # Load YAML file
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)

        # Override with environment variables
        config_data = cls._override_with_env(config_data)

        # Create Config object
        return cls(
            monitoring=MonitoringConfig.from_dict(config_data.get("monitoring", {})),
            prometheus=PrometheusConfig.from_dict(config_data.get("prometheus", {})),
            alerts=AlertsConfig.from_dict(config_data.get("alerts", {})),
            notifications=NotificationConfig.from_dict(config_data.get("notifications", {})),
            logging=LoggingConfig.from_dict(config_data.get("logging", {})),
        )

    @staticmethod
    def _override_with_env(config_data: dict) -> dict:
        """Override configuration with environment variables."""
        # Prometheus settings
        if os.getenv("PROMETHEUS_ENABLED"):
            config_data.setdefault("prometheus", {})["enabled"] = os.getenv("PROMETHEUS_ENABLED").lower() == "true"
        if os.getenv("PROMETHEUS_PORT"):
            config_data.setdefault("prometheus", {})["port"] = int(os.getenv("PROMETHEUS_PORT"))

        # Alerts settings
        if os.getenv("ALERTS_ENABLED"):
            config_data.setdefault("alerts", {})["enabled"] = os.getenv("ALERTS_ENABLED").lower() == "true"

        # Logging settings
        if os.getenv("LOG_LEVEL"):
            config_data.setdefault("logging", {})["level"] = os.getenv("LOG_LEVEL")

        return config_data
