"""
Network monitoring module
"""

import asyncio
import logging
import subprocess
from typing import Dict, List, Optional

import psutil

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
        self.ping_success = Counter(
            "network_ping_success_total",
            "Total successful pings",
            ["target"]
        )
        self.ping_failure = Counter(
            "network_ping_failure_total",
            "Total failed pings",
            ["target"]
        )
        self.bandwidth_bytes = Gauge(
            "network_bandwidth_bytes",
            "Network bandwidth in bytes",
            ["direction", "interface"]
        )
        self.bandwidth_bytes_per_sec = Gauge(
            "network_bandwidth_bytes_per_sec",
            "Network bandwidth in bytes per second",
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
        self.port_status = Gauge(
            "network_port_status",
            "Network port status",
            ["target", "port"]
        )

        # Previous bandwidth for rate calculation
        self._prev_bandwidth: Dict[str, Dict[str, int]] = {}
        self._prev_time: Optional[float] = None

    async def start(self) -> None:
        """Start network monitoring."""
        self.logger.info("Starting network monitor...")
        self._running = True

        # Start monitoring tasks
        tasks = [
            asyncio.create_task(self._monitor_ping()),
            asyncio.create_task(self._monitor_bandwidth()),
            asyncio.create_task(self._monitor_connections()),
            asyncio.create_task(self._monitor_ports()),
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
                    latency, success, loss_ratio = await self._ping_with_stats(target.host)
                    
                    if success:
                        self.ping_success.labels(target=target.name).inc()
                        if latency is not None:
                            self.ping_latency.labels(target=target.name).observe(latency)
                        if loss_ratio is not None:
                            self.packet_loss_ratio.labels(target=target.name).set(loss_ratio)
                    else:
                        self.ping_failure.labels(target=target.name).inc()
                        
                except Exception as e:
                    self.logger.error(f"Error pinging {target.name}: {e}")
                    self.ping_failure.labels(target=target.name).inc()

            await asyncio.sleep(interval)

    async def _monitor_bandwidth(self) -> None:
        """Monitor network bandwidth."""
        interval = self.config.intervals.get("bandwidth", 10)

        while self._running:
            try:
                current_time = asyncio.get_event_loop().time()
                
                # Get network statistics
                stats = self._get_network_stats()
                
                for interface, data in stats.items():
                    # Set current values
                    self.bandwidth_bytes.labels(
                        direction="rx",
                        interface=interface
                    ).set(data.get("bytes_recv", 0))
                    self.bandwidth_bytes.labels(
                        direction="tx",
                        interface=interface
                    ).set(data.get("bytes_sent", 0))
                    
                    # Calculate rate if we have previous data
                    if interface in self._prev_bandwidth and self._prev_time:
                        time_delta = current_time - self._prev_time
                        if time_delta > 0:
                            prev_data = self._prev_bandwidth[interface]
                            
                            rx_delta = data.get("bytes_recv", 0) - prev_data.get("bytes_recv", 0)
                            tx_delta = data.get("bytes_sent", 0) - prev_data.get("bytes_sent", 0)
                            
                            self.bandwidth_bytes_per_sec.labels(
                                direction="rx",
                                interface=interface
                            ).set(rx_delta / time_delta)
                            self.bandwidth_bytes_per_sec.labels(
                                direction="tx",
                                interface=interface
                            ).set(tx_delta / time_delta)
                
                # Store current data for next iteration
                self._prev_bandwidth = stats
                self._prev_time = current_time
                
            except Exception as e:
                self.logger.error(f"Error monitoring bandwidth: {e}")

            await asyncio.sleep(interval)

    async def _monitor_connections(self) -> None:
        """Monitor network connections."""
        while self._running:
            try:
                # Get connection statistics
                stats = self._get_connection_stats()
                for state, count in stats.items():
                    self.connection_count.labels(state=state).set(count)
            except Exception as e:
                self.logger.error(f"Error monitoring connections: {e}")

            await asyncio.sleep(10)

    async def _monitor_ports(self) -> None:
        """Monitor port status."""
        while self._running:
            for target in self.config.targets:
                try:
                    is_open = await self._check_port(target.host, target.port)
                    self.port_status.labels(
                        target=target.name,
                        port=str(target.port)
                    ).set(1 if is_open else 0)
                except Exception as e:
                    self.logger.error(f"Error checking port {target.name}:{target.port}: {e}")
                    self.port_status.labels(
                        target=target.name,
                        port=str(target.port)
                    ).set(0)
            
            await asyncio.sleep(30)

    async def _ping_with_stats(self, host: str) -> tuple[Optional[float], bool, Optional[float]]:
        """Ping a host and return latency, success, and packet loss ratio."""
        try:
            # Send 5 pings for statistics
            proc = await asyncio.create_subprocess_exec(
                "ping",
                "-c", "5",
                "-W", "1",
                host,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode == 0:
                output = stdout.decode()
                
                # Parse ping output
                # Example: "5 packets transmitted, 5 packets received, 0.0% packet loss"
                # "round-trip min/avg/max/stddev = 1.234/2.345/3.456/0.789 ms"
                
                success = True
                loss_ratio = None
                latency = None
                
                # Extract packet loss
                if "packet loss" in output:
                    loss_part = output.split("packet loss")[0].split()[-1]
                    try:
                        loss_ratio = float(loss_part.rstrip('%')) / 100.0
                    except (ValueError, IndexError):
                        pass
                
                # Extract latency (average)
                if "avg" in output:
                    try:
                        # Find the line with avg
                        for line in output.split('\n'):
                            if "avg" in line:
                                # Extract the average value
                                parts = line.split('avg=')[1].split('/')[0]
                                latency = float(parts.strip())
                                break
                    except (ValueError, IndexError):
                        pass
                
                return latency, success, loss_ratio
            else:
                return None, False, None
                
        except Exception as e:
            self.logger.debug(f"Error pinging {host}: {e}")
            return None, False, None

    async def _check_port(self, host: str, port: int) -> bool:
        """Check if a port is open."""
        try:
            # Use timeout for connection
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=2.0
            )
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return False
        except Exception as e:
            self.logger.debug(f"Error checking port {host}:{port}: {e}")
            return False

    def _get_network_stats(self) -> Dict[str, Dict[str, int]]:
        """Get network statistics."""
        stats = {}
        net_io = psutil.net_io_counters(pernic=True)
        
        for interface, counters in net_io.items():
            # Skip loopback and virtual interfaces
            if interface.startswith(('lo', 'docker', 'br-', 'veth')):
                continue
                
            stats[interface] = {
                "bytes_recv": counters.bytes_recv,
                "bytes_sent": counters.bytes_sent,
                "packets_recv": counters.packets_recv,
                "packets_sent": counters.packets_sent,
            }
        
        return stats

    def _get_connection_stats(self) -> Dict[str, int]:
        """Get connection statistics."""
        stats = {
            "ESTABLISHED": 0,
            "SYN_SENT": 0,
            "SYN_RECV": 0,
            "FIN_WAIT1": 0,
            "FIN_WAIT2": 0,
            "TIME_WAIT": 0,
            "CLOSE": 0,
            "CLOSE_WAIT": 0,
            "LAST_ACK": 0,
            "LISTEN": 0,
            "CLOSING": 0,
        }
        
        try:
            for conn in psutil.net_connections():
                status = conn.status
                if status in stats:
                    stats[status] += 1
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            self.logger.warning("Access denied or no such process while getting network connections")
        
        return stats
