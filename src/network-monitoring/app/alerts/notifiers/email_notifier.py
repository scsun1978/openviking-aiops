"""
Email notifier module - Send alert notifications via email
"""

import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

from app.alerts.rule_evaluator import Alert


class EmailNotifier:
    """Send alert notifications via email."""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        from_address: str,
        to_address: Optional[str] = None
    ):
        """Initialize email notifier."""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.from_address = from_address
        self.to_address = to_address or from_address
        self.logger = logging.getLogger(__name__)

    async def send(self, alert: Alert) -> None:
        """Send email notification for alert."""
        try:
            # Create message
            message = self._create_message(alert)

            # Send email
            await asyncio.to_thread(self._send_smtp, message)

            self.logger.info(f"Email notification sent for alert: {alert.name}")
        except Exception as e:
            self.logger.error(f"Failed to send email notification: {e}")

    def _create_message(self, alert: Alert) -> MIMEMultipart:
        """Create email message from alert."""
        message = MIMEMultipart("alternative")
        message["From"] = self.from_address
        message["To"] = self.to_address

        # Subject
        subject = f"[{alert.severity.upper()}] {alert.name}"
        if alert.state == "resolved":
            subject = f"[RESOLVED] {subject}"
        message["Subject"] = subject

        # Body
        body = self._format_alert_body(alert)
        message.attach(MIMEText(body, "plain"))

        return message

    def _format_alert_body(self, alert: Alert) -> str:
        """Format alert body."""
        lines = [
            f"Alert: {alert.name}",
            f"Severity: {alert.severity}",
            f"State: {alert.state}",
            f"Message: {alert.message}",
            f"Value: {alert.value}",
            f"Labels: {', '.join(f'{k}={v}' for k, v in alert.labels.items())}",
            f"Start Time: {alert.start_time.isoformat()}",
            f"Last Update: {alert.last_update.isoformat()}"
        ]
        return "\n".join(lines)

    def _send_smtp(self, message: MIMEMultipart) -> None:
        """Send email via SMTP."""
        with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(message)
            server.quit()
