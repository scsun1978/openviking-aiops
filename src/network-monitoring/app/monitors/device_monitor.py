"""
Device monitoring module
"""

import asyncio
import logging
from typing import Dict, Optional

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
        self.cpu_cores = Gauge(
            "cpu_cores_count",
            "Number of CPU cores"
        )
        self.cpu_frequency = Gauge(
            "cpu_frequency_mhz",
            "CPU frequency in MHz",
            ["core"]
        )
        self.memory_usage = Gauge(
            "memory_usage_ratio",
            "Memory usage ratio"
        )
        self.memory_total = Gauge(
            "memory_total_bytes",
            "Total memory in bytes"
        )
        self.memory_available = Gauge(
            "memory_available_bytes",
            "Available memory in bytes"
        )
        self.disk_usage = Gauge(
            "disk_usage_ratio",
            "Disk usage ratio",
            ["mountpoint"]
        )
        self.disk_total = Gauge(
            "disk_total_bytes",
            "Total disk space in bytes",
            ["mountpoint"]
        )
        self.disk_used = Gauge(
            "disk_used_bytes",
            "Used disk space in bytes",
            ["mountpoint"]
        )
        self.disk_free = Gauge(
            "disk_free_bytes",
            "Free disk space in bytes",
            ["mountpoint"]
        )
        self.temperature_celsius = Gauge(
            "device_temperature_celsius",
            "Device temperature in Celsius",
            ["sensor"]
        )
        self.power_status = Gauge(
            "device_power_status",
            "Device power status (1=on, 0=off)"
        )
        self.uptime_seconds = Gauge(
            "device_uptime_seconds",
            "Device uptime in seconds"
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
            asyncio.create_task(self._monitor_temperature()),
            asyncio.create_task(self._monitor_power()),
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
                # CPU usage percentage
                cpu_percent = psutil.cpu_percent(interval=1)
                self.cpu_usage.set(cpu_percent / 100.0)
                
                # Number of CPU cores
                cpu_count = psutil.cpu_count()
                self.cpu_cores.set(cpu_count)
                
                # CPU frequency
                cpu_freq = psutil.cpu_freq()
                if cpu_freq:
                    for core_idx in range(cpu_count):
                        freq_key = f"core_{core_idx}"
                        if hasattr(cpu_freq, 'current'):
                            self.cpu_frequency.labels(sensor=freq_key).set(cpu_freq.current / 1000.0)
                        elif hasattr(cpu_freq, 'min') and cpu_freq.min:
                            self.cpu_frequency.labels(sensor=freq_key).set(cpu_freq.min / 1000.0)
                    
            except Exception as e:
                self.logger.error(f"Error monitoring CPU: {e}")

            await asyncio.sleep(interval)

    async def _monitor_memory(self) -> None:
        """Monitor memory usage."""
        interval = self.config.intervals.get("memory", 10)

        while self._running:
            try:
                mem = psutil.virtual_memory()
                
                # Memory usage ratio
                self.memory_usage.set(mem.percent / 100.0)
                
                # Total and available memory
                self.memory_total.set(mem.total)
                self.memory_available.set(mem.available)
                
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
                        
                        # Disk usage ratio
                        self.disk_usage.labels(
                            mountpoint=partition.mountpoint
                        ).set(usage.percent / 100.0)
                        
                        # Total, used, and free disk space
                        self.disk_total.labels(
                            mountpoint=partition.mountpoint
                        ).set(usage.total)
                        self.disk_used.labels(
                            mountpoint=partition.mountpoint
                        ).set(usage.used)
                        self.disk_free.labels(
                            mountpoint=partition.mountpoint
                        ).set(usage.free)
                        
                    except Exception as e:
                        self.logger.error(f"Error monitoring disk {partition.mountpoint}: {e}")
            except Exception as e:
                self.logger.error(f"Error monitoring disk: {e}")

            await asyncio.sleep(interval)

    async def _monitor_temperature(self) -> None:
        """Monitor device temperature."""
        interval = 60  # Check temperature every minute

        while self._running:
            try:
                # Get temperature sensors
                temps = psutil.sensors_temperatures()
                
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            if hasattr(entry, 'current') and entry.current is not None:
                                sensor_name = f"{name}_{entry.label}" if hasattr(entry, 'label') else name
                                self.temperature_celsius.labels(sensor=sensor_name).set(entry.current)
                else:
                    # No temperature sensors available
                    self.logger.debug("No temperature sensors available on this system")
                    
            except Exception as e:
                self.logger.error(f"Error monitoring temperature: {e}")

            await asyncio.sleep(interval)

    async def _monitor_power(self) -> None:
        """Monitor power status."""
        interval = 60  # Check power status every minute

        while self._running:
            try:
                # Check battery status if available
                battery = psutil.sensors_battery()
                
                if battery:
                    # Battery is present
                    self.power_status.set(1 if battery.power_plugged else 0)
                    
                    self.logger.debug(f"Battery: {battery.percent}%, Power plugged: {battery.power_plugged}")
                else:
                    # No battery - assume always on (desktop/server)
                    self.power_status.set(1)
                    
            except Exception as e:
                self.logger.error(f"Error monitoring power: {e}")

            await asyncio.sleep(interval)

    def get_uptime_seconds(self) -> Optional[float]:
        """Get system uptime in seconds."""
        try:
            # Get boot time
            boot_time = psutil.boot_time()
            
            # Calculate uptime
            import time
            uptime = time.time() - boot_time
            
            self.uptime_seconds.set(uptime)
            return uptime
        except Exception as e:
            self.logger.error(f"Error getting uptime: {e}")
            return None
