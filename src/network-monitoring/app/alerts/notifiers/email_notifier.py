"""
Email notification module
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotifier:
    """Send email notifications."""

    def __init__(self, smtp_host: str, smtp_port: int, smtp_user: str, smtp_password: str):
        """Initialize email notifier."""
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.logger = logging.getLogger(__name__)

    async def send(self, to: str, subject: str, body: str) -> bool:
        """Send email notification."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.smtp_user
            msg["To"] = to
            msg["Subject"] = subject

            # Attach body
            msg.attach(MIMEText(body, "plain"))

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            self.logger.info(f"Email sent to {to}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send email to {to}: {e}")
            return False
