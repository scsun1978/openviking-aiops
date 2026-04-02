"""
Webhook notifier module - Send alert notifications via HTTP webhook
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any
import logging

from app.alerts.rule_evaluator import Alert


class WebhookNotifier:
    """Send alert notifications via HTTP webhook."""

    def __init__(self, url: str, timeout: int = 10):
        """Initialize webhook notifier."""
        self.url = url
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    async def send(self, alert: Alert) -> None:
        """Send webhook notification for alert."""
        try:
            # Create payload
            payload = self._create_payload(alert)

            # Send webhook
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url,
                    json=payload,
                    timeout=self.timeout
                ) as response:
                    if response.status >= 200 and response.status < 300:
                        self.logger.info(f"Webhook notification sent for alert: {alert.name}")
                    else:
                        self.logger.error(f"Webhook failed with status {response.status}")
        except Exception as e:
            self.logger.error(f"Failed to send webhook notification: {e}")

    def _create_payload(self, alert: Alert) -> Dict[str, Any]:
        """Create webhook payload from alert."""
        return {
            "alert_name": alert.name,
            "severity": alert.severity,
            "state": alert.state,
            "message": alert.message,
            "value": alert.value,
            "labels": alert.labels,
            "start_time": alert.start_time.isoformat(),
            "last_update": alert.last_update.isoformat(),
            "timestamp": alert.last_update.isoformat()
        }
