"""
Telegram notifier module - Send alert notifications via Telegram bot
"""

import asyncio
import aiohttp
from typing import Optional
import logging

from app.alerts.rule_evaluator import Alert


class TelegramNotifier:
    """Send alert notifications via Telegram bot."""

    def __init__(
        self,
        bot_token: str,
        chat_id: str,
        parse_mode: str = "HTML",
        disable_web_page_preview: bool = True
    ):
        """Initialize Telegram notifier."""
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.logger = logging.getLogger(__name__)

    async def send(self, alert: Alert) -> None:
        """Send Telegram notification for alert."""
        try:
            # Create message
            message = self._create_message(alert)

            # Send message
            await self._send_telegram_message(message)

            self.logger.info(f"Telegram notification sent for alert: {alert.name}")
        except Exception as e:
            self.logger.error(f"Failed to send Telegram notification: {e}")

    def _create_message(self, alert: Alert) -> str:
        """Create Telegram message from alert."""
        # Choose emoji based on severity
        emoji_map = {
            "info": "ℹ️",
            "warning": "⚠️",
            "critical": "🚨"
        }
        emoji = emoji_map.get(alert.severity, "⚠️")

        # Format labels
        labels_str = " | ".join(f"{k}=<b>{v}</b>" for k, v in alert.labels.items())

        # Create message
        if alert.state == "resolved":
            message = f"""✅ <b>Resolved</b>: {alert.name}

<b>Severity</b>: {alert.severity}
<b>Message</b>: {alert.message}
<b>Duration</b>: {(alert.last_update - alert.start_time).total_seconds():.0f} seconds
<b>Labels</b>: {labels_str}"""
        else:
            message = f"""{emoji} <b>{alert.severity.upper()}</b>: {alert.name}

<b>Severity</b>: {alert.severity}
<b>State</b>: {alert.state}
<b>Message</b>: {alert.message}
<b>Value</b>: {alert.value}
<b>Labels</b>: {labels_str}
<b>Start Time</b>: {alert.start_time.strftime('%Y-%m-%d %H:%M:%S')}"""

        return message

    async def _send_telegram_message(self, message: str) -> None:
        """Send message via Telegram API."""
        url = f"{self.base_url}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": self.parse_mode,
            "disable_web_page_preview": self.disable_web_page_preview
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=10) as response:
                data = await response.json()

                if not data.get("ok"):
                    self.logger.error(f"Telegram API error: {data.get('description', 'Unknown error')}")
