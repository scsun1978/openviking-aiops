"""
Prometheus metrics collector module
"""

import asyncio
import logging
from contextlib import asynccontextmanager

from prometheus_client import start_http_server

from app.utils.config import PrometheusConfig


class MetricsCollector:
    """Collect and expose Prometheus metrics."""

    def __init__(self, config: PrometheusConfig):
        """Initialize metrics collector."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._running = False

    async def start(self) -> None:
        """Start metrics server."""
        if not self.config.enabled:
            self.logger.info("Prometheus metrics disabled")
            return

        self.logger.info(f"Starting Prometheus metrics server on port {self.config.port}")
        self._running = True

        # Start HTTP server
        try:
            start_http_server(self.config.port)
            self.logger.info(f"Prometheus metrics server started on port {self.config.port}")
        except Exception as e:
            self.logger.error(f"Failed to start metrics server: {e}")

    async def stop(self) -> None:
        """Stop metrics server."""
        if self._running:
            self.logger.info("Stopping Prometheus metrics server...")
            self._running = False
