"""
Webhook notification module
"""

import logging

import aiohttp


class WebhookNotifier:
    """Send webhook notifications."""

    def __init__(self, url: str):
        """Initialize webhook notifier."""
        self.url = url
        self.logger = logging.getLogger(__name__)

    async def send(self, payload: dict) -> bool:
        """Send webhook notification."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, json=payload) as response:
                    if response.status == 200:
                        self.logger.info(f"Webhook sent successfully to {self.url}")
                        return True
                    else:
                        self.logger.error(f"Webhook failed with status {response.status}")
                        return False
        except Exception as e:
            self.logger.error(f"Failed to send webhook to {self.url}: {e}")
            return False
