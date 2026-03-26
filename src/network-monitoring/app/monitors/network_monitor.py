"""
Network monitoring module
"""

import asyncio
import logging
import subprocess
from typing import Optional

from prometheus_client import Counter, Histogram, Gauge

from app.utils.config import MonitoringConfig


class NetworkMonitor:
    """Monitor network status."""

    def __init__(self, config: MonitoringConfig, metrics_collector):
        """Initialize network monitor."""
        self.config = config
        self.metrics_collector = metrics_collector
        self.logger = logging.getLogger(__name__)
        self._running = False

        # Prometheus metrics
        self.ping_latency = Histogram(
            "network_ping_latency_ms",
            "Network ping latency in milliseconds",
            ["target"]
        )
        self.bandwidth_bytes = Gauge(
            "network_bandwidth_bytes",
            "Network bandwidth in bytes",
            ["direction", "interface"]
        )
        self.packet_loss_ratio = Gauge(
            "network_packet_loss_ratio",
            "Network packet loss ratio",
            ["target"]
        )
        self.connection_count = Gauge(
            "network_connections_count",
            "Number of active network connections",
            ["state"]
        )

    async def start(self) -> None:
        """Start network monitoring."""
        self.logger.info("Starting network monitor...")
        self._running = True

        # Start monitoring tasks
        tasks = [
            asyncio.create_task(self._monitor_ping()),
            asyncio.create_task(self._monitor_bandwidth()),
            asyncio.create_task(self._monitor_connections()),
        ]

        # Wait for all tasks to complete (they won't unless stopped)
        await asyncio.gather(*tasks, return_exceptions=True)

    async def stop(self) -> None:
        """Stop network monitoring."""
        self.logger.info("Stopping network monitor...")
        self._running = False

    async def _monitor_ping(self) -> None:
        """Monitor network ping latency."""
        interval = self.config.intervals.get("ping", 60)

        while self._running:
            for target in self.config.targets:
                try:
                    latency = await self._ping(target.host)
                    if latency is not None:
                        self.ping_latency.labels(target=target.name).observe(latency)
                except Exception as e:
                    self.logger.error(f"Error pinging {target.name}: {e}")

            await asyncio.sleep(interval)

    async def _monitor_bandwidth(self) -> None:
        """Monitor network bandwidth."""
        interval = self.config.intervals.get("bandwidth", 10)

        while self._running:
            try:
                # Get network statistics
                stats = await self._get_network_stats()
                for interface, data in stats.items():
                    self.bandwidth_bytes.labels(
                        direction="rx",
                        interface=interface
                    ).set(data.get("bytes_recv", 0))
                    self.bandwidth_bytes.labels(
                        direction="tx",
                        interface=interface
                    ).set(data.get("bytes_sent", 0))
            except Exception as e:
                self.logger.error(f"Error monitoring bandwidth: {e}")

            await asyncio.sleep(interval)

    async def _monitor_connections(self) -> None:
        """Monitor network connections."""
        while self._running:
            try:
                # Get connection statistics
                stats = await self._get_connection_stats()
                for state, count in stats.items():
                    self.connection_count.labels(state=state).set(count)
            except Exception as e:
                self.logger.error(f"Error monitoring connections: {e}")

            await asyncio.sleep(10)

    async def _ping(self, host: str) -> Optional[float]:
        """Ping a host and return latency."""
        try:
            proc = await asyncio.create_subprocess_exec(
                "ping",
                "-c", "1",
                "-W", "1",
                host,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode == 0:
                # Parse ping output
                output = stdout.decode()
                if "time=" in output:
                    # Extract latency
                    parts = output.split("time=")[1].split()[0]
                    return float(parts)
        except Exception as e:
            self.logger.error(f"Error pinging {host}: {e}")

        return None

    async def _get_network_stats(self) -> dict:
        """Get network statistics."""
        # This is a placeholder - implement actual network stats collection
        return {
            "eth0": {"bytes_recv": 0, "bytes_sent": 0},
            "lo": {"bytes_recv": 0, "bytes_sent": 0},
        }

    async def _get_connection_stats(self) -> dict:
        """Get connection statistics."""
        # This is a placeholder - implement actual connection stats collection
        return {
            "ESTABLISHED": 0,
            "TIME_WAIT": 0,
            "CLOSE_WAIT": 0,
        }
