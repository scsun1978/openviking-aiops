"""
Main entry point for the Network Monitoring Service
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path

from app.utils.config import Config
from app.utils.logger import setup_logging
from app.monitors.network_monitor import NetworkMonitor
from app.monitors.device_monitor import DeviceMonitor
from app.metrics.metrics_collector import MetricsCollector
from app.alerts.alert_manager import AlertManager


# Global variables for graceful shutdown
shutdown_event = asyncio.Event()


async def main() -> None:
    """Main entry point for the network monitoring service."""
    # Load configuration
    config = Config.load()

    # Setup logging
    setup_logging(config.logging)
    logger = logging.getLogger(__name__)

    logger.info("Starting Network Monitoring Service v0.1.0")

    # Initialize components
    metrics_collector = MetricsCollector(config.prometheus)
    network_monitor = NetworkMonitor(config.monitoring, metrics_collector)
    device_monitor = DeviceMonitor(config.monitoring, metrics_collector)
    alert_manager = AlertManager(config.alerts, config.notifications)

    # Start all monitors
    logger.info("Starting monitors...")
    await network_monitor.start()
    await device_monitor.start()
    await metrics_collector.start()
    await alert_manager.start()

    logger.info("All monitors started successfully")
    logger.info(f"Prometheus metrics available at http://0.0.0.0:{config.prometheus.port}{config.prometheus.path}")

    # Wait for shutdown signal
    await shutdown_event.wait()

    # Graceful shutdown
    logger.info("Shutting down...")
    await network_monitor.stop()
    await device_monitor.stop()
    await metrics_collector.stop()
    await alert_manager.stop()

    logger.info("Shutdown complete")


def signal_handler(signum: int, frame) -> None:
    """Handle shutdown signals."""
    logger = logging.getLogger(__name__)
    logger.info(f"Received signal {signum}, initiating shutdown...")
    shutdown_event.set()


if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger = logging.getLogger(__name__)
        logger.info("Received keyboard interrupt, shutting down...")
        sys.exit(0)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
