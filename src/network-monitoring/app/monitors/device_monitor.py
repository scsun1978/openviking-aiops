"""
Device monitoring module
"""

import asyncio
import logging
from typing import Optional

import psutil

from prometheus_client import Gauge

from app.utils.config import MonitoringConfig


class DeviceMonitor:
    """Monitor device health."""

    def __init__(self, config: MonitoringConfig, metrics_collector):
        """Initialize device monitor."""
        self.config = config
        self.metrics_collector = metrics_collector
        self.logger = logging.getLogger(__name__)
        self._running = False

        # Prometheus metrics
        self.cpu_usage = Gauge(
            "cpu_usage_ratio",
            "CPU usage ratio"
        )
        self.memory_usage = Gauge(
            "memory_usage_ratio",
            "Memory usage ratio"
        )
        self.disk_usage = Gauge(
            "disk_usage_ratio",
            "Disk usage ratio",
            ["mountpoint"]
        )

    async def start(self) -> None:
        """Start device monitoring."""
        self.logger.info("Starting device monitor...")
        self._running = True

        # Start monitoring tasks
        tasks = [
            asyncio.create_task(self._monitor_cpu()),
            asyncio.create_task(self._monitor_memory()),
            asyncio.create_task(self._monitor_disk()),
        ]

        # Wait for all tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)

    async def stop(self) -> None:
        """Stop device monitoring."""
        self.logger.info("Stopping device monitor...")
        self._running = False

    async def _monitor_cpu(self) -> None:
        """Monitor CPU usage."""
        interval = self.config.intervals.get("cpu", 10)

        while self._running:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                self.cpu_usage.set(cpu_percent / 100.0)
            except Exception as e:
                self.logger.error(f"Error monitoring CPU: {e}")

            await asyncio.sleep(interval)

    async def _monitor_memory(self) -> None:
        """Monitor memory usage."""
        interval = self.config.intervals.get("memory", 10)

        while self._running:
            try:
                mem = psutil.virtual_memory()
                self.memory_usage.set(mem.percent / 100.0)
            except Exception as e:
                self.logger.error(f"Error monitoring memory: {e}")

            await asyncio.sleep(interval)

    async def _monitor_disk(self) -> None:
        """Monitor disk usage."""
        interval = self.config.intervals.get("disk", 60)

        while self._running:
            try:
                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        self.disk_usage.labels(
                            mountpoint=partition.mountpoint
                        ).set(usage.percent / 100.0)
                    except Exception as e:
                        self.logger.error(f"Error monitoring disk {partition.mountpoint}: {e}")
            except Exception as e:
                self.logger.error(f"Error monitoring disk: {e}")

            await asyncio.sleep(interval)
