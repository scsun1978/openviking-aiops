"""
Alert manager module - Manage alerts and notifications
"""

import asyncio
import logging
from typing import List, Dict
from datetime import datetime

from app.alerts.rule_parser import RuleParser, AlertRule
from app.alerts.rule_evaluator import RuleEvaluator, Alert
from app.alerts.notifiers.email_notifier import EmailNotifier
from app.alerts.notifiers.webhook_notifier import WebhookNotifier
from app.alerts.notifiers.telegram_notifier import TelegramNotifier
from app.utils.config import AlertsConfig, NotificationConfig


class AlertManager:
    """Manage alerts and notifications."""

    def __init__(
        self,
        alerts_config: AlertsConfig,
        notifications_config: NotificationConfig,
        metrics_collector
    ):
        """Initialize alert manager."""
        self.config = alerts_config
        self.notifications_config = notifications_config
        self.metrics_collector = metrics_collector
        self.logger = logging.getLogger(__name__)
        self._running = False

        # Components
        self.rule_parser = RuleParser()
        self.rule_evaluator = RuleEvaluator(metrics_collector)
        self.notifiers = []

        # Load notifiers
        self._load_notifiers()

    def _load_notifiers(self) -> None:
        """Load notification notifiers based on configuration."""
        self.notifiers = []

        # Email notifier
        if self.notifications_config.email.enabled:
            self.notifiers.append(EmailNotifier(
                self.notifications_config.email.smtp_server,
                self.notifications_config.email.smtp_port,
                self.notifications_config.email.smtp_username,
                self.notifications_config.email.smtp_password,
                self.notifications_config.email.from_address
            ))
            self.logger.info("Email notifier loaded")

        # Webhook notifier
        if self.notifications_config.webhook.enabled:
            self.notifiers.append(WebhookNotifier(
                self.notifications_config.webhook.url,
                self.notifications_config.webhook.timeout
            ))
            self.logger.info("Webhook notifier loaded")

        # Telegram notifier
        if self.notifications_config.telegram.enabled:
            self.notifiers.append(TelegramNotifier(
                self.notifications_config.telegram.bot_token,
                self.notifications_config.telegram.chat_id
            ))
            self.logger.info("Telegram notifier loaded")

    async def start(self) -> None:
        """Start alert manager."""
        if not self.config.enabled:
            self.logger.info("Alert manager disabled")
            return

        self.logger.info("Starting alert manager...")
        self._running = True

        # Load alert rules
        await self._load_alert_rules()

        # Start evaluation loop
        asyncio.create_task(self._evaluation_loop())

    async def stop(self) -> None:
        """Stop alert manager."""
        if self._running:
            self.logger.info("Stopping alert manager...")
            self._running = False

    async def _load_alert_rules(self) -> None:
        """Load alert rules from configuration file."""
        try:
            with open(self.config.rules_file, 'r') as f:
                content = f.read()

            # Parse rules based on file extension
            if self.config.rules_file.endswith('.yaml') or self.config.rules_file.endswith('.yml'):
                rules = self.rule_parser.parse_from_yaml(content)
            else:
                rules = self.rule_parser.parse_from_json(content)

            # Load rules into evaluator
            await self.rule_evaluator.load_rules(rules)
            self.logger.info(f"Loaded {len(rules)} alert rules")

        except Exception as e:
            self.logger.error(f"Failed to load alert rules: {e}")

    async def _evaluation_loop(self) -> None:
        """Main evaluation loop."""
        while self._running:
            try:
                # Evaluate all rules
                new_alerts = await self.rule_evaluator.evaluate_rules()

                # Send notifications for new alerts
                for alert in new_alerts:
                    await self._send_notifications(alert)

                # Check for resolved alerts
                await self._check_resolved_alerts()

            except Exception as e:
                self.logger.error(f"Error in evaluation loop: {e}")

            # Wait before next evaluation
            await asyncio.sleep(self.config.evaluation_interval)

    async def _send_notifications(self, alert: Alert) -> None:
        """Send notifications for an alert."""
        for notifier in self.notifiers:
            try:
                await notifier.send(alert)
            except Exception as e:
                self.logger.error(f"Failed to send notification via {notifier}: {e}")

    async def _check_resolved_alerts(self) -> None:
        """Check if any alerts should be resolved."""
        active_alerts = self.rule_evaluator.get_active_alerts()

        for alert in active_alerts:
            # Re-evaluate the rule to see if it's still firing
            # This is a simplified check - in production, you'd have more sophisticated logic
            rule = next((r for r in self.rule_evaluator._rules if r.name == alert.name), None)
            if rule:
                triggered = await self.rule_evaluator._evaluate_rule(rule)
                if not triggered:
                    await self.rule_evaluator.resolve_alert(alert.name)
                    # Send resolved notification
                    alert.state = "resolved"
                    await self._send_notifications(alert)

    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts."""
        return self.rule_evaluator.get_active_alerts()

    def get_alert_history(self, limit: int = 100) -> List[Alert]:
        """Get alert history."""
        return self.rule_evaluator.get_alert_history(limit)
