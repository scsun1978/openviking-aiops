"""
Telegram notification module
"""

import logging

import aiohttp


class TelegramNotifier:
    """Send Telegram notifications."""

    def __init__(self, bot_token: str, chat_id: str):
        """Initialize Telegram notifier."""
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.logger = logging.getLogger(__name__)
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    async def send(self, message: str) -> bool:
        """Send Telegram notification."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json={
                        "chat_id": self.chat_id,
                        "text": message,
                        "parse_mode": "HTML"
                    }
                ) as response:
                    if response.status == 200:
                        self.logger.info("Telegram message sent successfully")
                        return True
                    else:
                        self.logger.error(f"Telegram API failed with status {response.status}")
                        return False
        except Exception as e:
            self.logger.error(f"Failed to send Telegram message: {e}")
            return False
