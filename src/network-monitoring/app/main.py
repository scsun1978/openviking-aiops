"""
Network monitoring service main entry point
"""

import asyncio
import signal
import sys
import logging
from pathlib import Path

from app.utils.config import (
    MonitoringConfig,
    AlertsConfig,
    NotificationConfig,
    load_config
)
from app.utils.logger import setup_logger
from app.monitors.network_monitor import NetworkMonitor
from app.monitors.device_monitor import DeviceMonitor
from app.alerts.alert_manager import AlertManager
from app.metrics.metrics_collector import MetricsCollector


class NetworkMonitoringService:
    """Main network monitoring service."""

    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize monitoring service."""
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self._running = False

        # Components
        self.network_monitor: NetworkMonitor = None
        self.device_monitor: DeviceMonitor = None
        self.alert_manager: AlertManager = None
        self.metrics_collector: MetricsCollector = None

        # Configuration
        self.monitoring_config: MonitoringConfig = None
        self.alerts_config: AlertsConfig = None
        self.notifications_config: NotificationConfig = None

    async def start(self) -> None:
        """Start monitoring service."""
        self.logger.info("Starting network monitoring service...")
        self._running = True

        # Load configuration
        await self._load_configuration()

        # Setup logging
        setup_logger(self.config_path)

        # Initialize metrics collector
        self.metrics_collector = MetricsCollector()
        await self.metrics_collector.start()

        # Initialize monitors
        self.network_monitor = NetworkMonitor(
            self.monitoring_config,
            self.metrics_collector
        )
        self.device_monitor = DeviceMonitor(
            self.monitoring_config,
            self.metrics_collector
        )

        # Initialize alert manager
        self.alert_manager = AlertManager(
            self.alerts_config,
            self.notifications_config,
            self.metrics_collector
        )

        # Start components
        await self.network_monitor.start()
        await self.device_monitor.start()
        await self.alert_manager.start()

        # Start Prometheus metrics server
        from prometheus_client import start_http_server

        try:
            start_http_server(
                port=self.monitoring_config.prometheus.port,
                addr=self.monitoring_config.prometheus.host
            )
            self.logger.info(f"Prometheus metrics server started on {self.monitoring_config.prometheus.host}:{self.monitoring_config.prometheus.port}")
        except Exception as e:
            self.logger.error(f"Failed to start Prometheus server: {e}")

        self.logger.info("Network monitoring service started")

    async def stop(self) -> None:
        """Stop monitoring service."""
        if not self._running:
            return

        self.logger.info("Stopping network monitoring service...")
        self._running = False

        # Stop components
        if self.network_monitor:
            await self.network_monitor.stop()
        if self.device_monitor:
            await self.device_monitor.stop()
        if self.alert_manager:
            await self.alert_manager.stop()
        if self.metrics_collector:
            await self.metrics_collector.stop()

        self.logger.info("Network monitoring service stopped")

    async def _load_configuration(self) -> None:
        """Load configuration from file."""
        try:
            configs = load_config(self.config_path)
            self.monitoring_config = configs["monitoring"]
            self.alerts_config = configs["alerts"]
            self.notifications_config = configs["notifications"]
            self.logger.info("Configuration loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            sys.exit(1)

    async def run(self) -> None:
        """Run service until interrupted."""
        try:
            while self._running:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass


async def main():
    """Main entry point."""
    # Create service
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config/config.yaml"
    service = NetworkMonitoringService(config_path)

    # Setup signal handlers
    def signal_handler(signum, frame):
        service.logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(service.stop())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start service
    try:
        await service.start()
        await service.run()
    except KeyboardInterrupt:
        service.logger.info("Keyboard interrupt received")
    except Exception as e:
        service.logger.error(f"Service error: {e}")
        raise
    finally:
        await service.stop()


if __name__ == "__main__":
    asyncio.run(main())
