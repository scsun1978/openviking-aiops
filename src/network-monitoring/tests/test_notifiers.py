"""
Test notification notifiers
"""

import pytest
from unittest.mock import AsyncMock, patch
from app.alerts.rule_evaluator import Alert
from app.alerts.notifiers.email_notifier import EmailNotifier
from app.alerts.notifiers.webhook_notifier import WebhookNotifier
from app.alerts.notifiers.telegram_notifier import TelegramNotifier
from datetime import datetime


@pytest.fixture
def alert():
    """Create test alert."""
    return Alert(
        name="test_alert",
        severity="warning",
        message="Test alert message",
        labels={"service": "system", "host": "localhost"},
        state="firing",
        start_time=datetime.now(),
        last_update=datetime.now(),
        value=0.85
    )


def test_email_notifier_init():
    """Test email notifier initialization."""
    notifier = EmailNotifier(
        smtp_server="smtp.example.com",
        smtp_port=587,
        smtp_username="user@example.com",
        smtp_password="password",
        from_address="noreply@example.com"
    )

    assert notifier.smtp_server == "smtp.example.com"
    assert notifier.smtp_port == 587
    assert notifier.from_address == "noreply@example.com"


def test_email_notifier_message_creation(alert):
    """Test email message creation."""
    notifier = EmailNotifier(
        smtp_server="smtp.example.com",
        smtp_port=587,
        smtp_username="user@example.com",
        smtp_password="password",
        from_address="noreply@example.com"
    )

    message = notifier._create_message(alert)

    assert message["From"] == "noreply@example.com"
    assert "test_alert" in message["Subject"]
    assert "[WARNING]" in message["Subject"]


def test_webhook_notifier_init():
    """Test webhook notifier initialization."""
    notifier = WebhookNotifier(
        url="https://example.com/webhook",
        timeout=10
    )

    assert notifier.url == "https://example.com/webhook"
    assert notifier.timeout == 10


def test_webhook_notifier_payload_creation(alert):
    """Test webhook payload creation."""
    notifier = WebhookNotifier(
        url="https://example.com/webhook"
    )

    payload = notifier._create_payload(alert)

    assert payload["alert_name"] == "test_alert"
    assert payload["severity"] == "warning"
    assert payload["state"] == "firing"
    assert payload["value"] == 0.85
    assert payload["labels"] == {"service": "system", "host": "localhost"}


def test_telegram_notifier_init():
    """Test Telegram notifier initialization."""
    notifier = TelegramNotifier(
        bot_token="test_token",
        chat_id="123456789"
    )

    assert notifier.bot_token == "test_token"
    assert notifier.chat_id == "123456789"
    assert notifier.parse_mode == "HTML"


def test_telegram_notifier_message_creation_firing(alert):
    """Test Telegram message creation for firing alert."""
    notifier = TelegramNotifier(
        bot_token="test_token",
        chat_id="123456789"
    )

    message = notifier._create_message(alert)

    assert "test_alert" in message
    assert "⚠️" in message
    assert "WARNING" in message
    assert "<b>Severity</b>: warning" in message


def test_telegram_notifier_message_creation_resolved():
    """Test Telegram message creation for resolved alert."""
    resolved_alert = Alert(
        name="test_alert",
        severity="warning",
        message="Test alert message",
        labels={},
        state="resolved",
        start_time=datetime.now(),
        last_update=datetime.now(),
        value=0.85
    )

    notifier = TelegramNotifier(
        bot_token="test_token",
        chat_id="123456789"
    )

    message = notifier._create_message(resolved_alert)

    assert "test_alert" in message
    assert "✅" in message
    assert "<b>Resolved</b>" in message
    assert "[RESOLVED]" not in message  # State is shown as text, not in emoji


def test_telegram_notifier_emoji_mapping():
    """Test emoji mapping for different severities."""
    notifier = TelegramNotifier(
        bot_token="test_token",
        chat_id="123456789"
    )

    # Check that all severities have emojis
    for severity, emoji in [("info", "ℹ️"), ("warning", "⚠️"), ("critical", "🚨")]:
        alert = Alert(
            name=f"test_{severity}",
            severity=severity,
            message="Test",
            labels={},
            state="firing",
            start_time=datetime.now(),
            last_update=datetime.now(),
            value=0.0
        )

        message = notifier._create_message(alert)
        assert emoji in message, f"Emoji {emoji} not in message for severity {severity}"


def test_email_notifier_resolved_subject(alert):
    """Test email subject for resolved alert."""
    resolved_alert = Alert(
        name="test_alert",
        severity="warning",
        message="Test alert message",
        labels={},
        state="resolved",
        start_time=datetime.now(),
        last_update=datetime.now(),
        value=0.85
    )

    notifier = EmailNotifier(
        smtp_server="smtp.example.com",
        smtp_port=587,
        smtp_username="user@example.com",
        smtp_password="password",
        from_address="noreply@example.com"
    )

    message = notifier._create_message(resolved_alert)

    assert "[RESOLVED]" in message["Subject"]
