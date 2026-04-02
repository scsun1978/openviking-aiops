"""
Rule evaluator module - Evaluate alert rules and trigger alerts
"""

import asyncio
import time
import logging
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.alerts.rule_parser import (
    AlertRule, ThresholdCondition, TrendCondition
)


@dataclass
class Alert:
    """Active alert instance."""
    name: str
    severity: str
    message: str
    labels: Dict[str, str]
    state: str  # pending, firing, resolved
    start_time: datetime
    last_update: datetime
    value: Optional[float]


@dataclass
class MetricValue:
    """Metric value with timestamp."""
    metric: str
    value: float
    timestamp: datetime


class RuleEvaluator:
    """Evaluate alert rules and trigger alerts."""

    def __init__(self, metrics_collector):
        """Initialize rule evaluator."""
        self.metrics_collector = metrics_collector
        self.logger = logging.getLogger(__name__)
        self._running = False

        # Alert storage
        self._active_alerts: Dict[str, Alert] = {}
        self._alert_history: List[Alert] = []

        # Metric history for trend detection
        self._metric_history: Dict[str, List[MetricValue]] = {}

        # Rule state
        self._rules: List[AlertRule] = []

    async def load_rules(self, rules: List[AlertRule]) -> None:
        """Load alert rules."""
        self._rules = [rule for rule in rules if rule.enabled]
        self.logger.info(f"Loaded {len(self._rules)} alert rules")

    async def evaluate_rules(self) -> List[Alert]:
        """Evaluate all alert rules and return new/updated alerts."""
        new_alerts = []

        for rule in self._rules:
            try:
                triggered = await self._evaluate_rule(rule)
                if triggered:
                    alert = await self._update_alert(rule, triggered)
                    if alert:
                        new_alerts.append(alert)
            except Exception as e:
                self.logger.error(f"Failed to evaluate rule {rule.name}: {e}")

        return new_alerts

    async def _evaluate_rule(self, rule: AlertRule) -> Optional[Dict]:
        """Evaluate a single alert rule."""
        results = []

        for condition in rule.conditions:
            if isinstance(condition, ThresholdCondition):
                result = await self._evaluate_threshold(condition)
                results.append(result)
            elif isinstance(condition, TrendCondition):
                result = await self._evaluate_trend(condition)
                results.append(result)

        # Aggregate results
        if rule.aggregator == "AND":
            triggered = all(results)
        else:  # OR
            triggered = any(results)

        if triggered:
            return {
                "name": rule.name,
                "severity": rule.severity,
                "message": rule.message,
                "labels": rule.labels,
                "value": results[0].get("value", 0) if results else 0
            }

        return None

    async def _evaluate_threshold(self, condition: ThresholdCondition) -> Dict:
        """Evaluate threshold condition."""
        # Get current metric value
        value = await self._get_metric_value(condition.metric)
        if value is None:
            return {"triggered": False}

        # Check threshold
        triggered = False
        if condition.operator == ">":
            triggered = value > condition.threshold
        elif condition.operator == "<":
            triggered = value < condition.threshold
        elif condition.operator == "=":
            triggered = value == condition.threshold
        elif condition.operator == "!=":
            triggered = value != condition.threshold
        elif condition.operator == ">=":
            triggered = value >= condition.threshold
        elif condition.operator == "<=":
            triggered = value <= condition.threshold

        return {"triggered": triggered, "value": value}

    async def _evaluate_trend(self, condition: TrendCondition) -> Dict:
        """Evaluate trend condition."""
        # Get metric history
        history = self._metric_history.get(condition.metric, [])
        if len(history) < 2:
            return {"triggered": False}

        # Calculate trend
        current = history[-1].value
        previous = history[0].value

        if previous == 0:
            return {"triggered": False}

        rate = (current - previous) / abs(previous) * 100  # percentage

        triggered = False
        if condition.type == "growth" and rate > condition.rate:
            triggered = True
        elif condition.type == "decline" and rate < -condition.rate:
            triggered = True

        return {"triggered": triggered, "value": current}

    async def _get_metric_value(self, metric: str) -> Optional[float]:
        """Get current metric value from collector."""
        # Placeholder - implement actual metric retrieval
        # This would query the Prometheus metrics collector
        return None

    async def _update_alert(self, rule: AlertRule, trigger_data: Dict) -> Optional[Alert]:
        """Update or create alert based on rule trigger."""
        now = datetime.now()
        alert_key = rule.name

        # Check if alert already exists
        if alert_key in self._active_alerts:
            existing_alert = self._active_alerts[alert_key]
            existing_alert.last_update = now
            existing_alert.value = trigger_data.get("value")
            return None  # No new alert

        # Check suppression
        last_alert = self._get_last_alert(alert_key)
        if last_alert and (now - last_alert.start_time).total_seconds() < rule.suppress_duration:
            self.logger.info(f"Alert {alert_key} suppressed")
            return None

        # Create new alert
        alert = Alert(
            name=alert_key,
            severity=trigger_data.get("severity", "warning"),
            message=trigger_data.get("message", ""),
            labels=trigger_data.get("labels", {}),
            state="firing",
            start_time=now,
            last_update=now,
            value=trigger_data.get("value")
        )

        self._active_alerts[alert_key] = alert
        self._alert_history.append(alert)
        self.logger.warning(f"Alert triggered: {alert_key} - {alert.message}")

        return alert

    def _get_last_alert(self, alert_key: str) -> Optional[Alert]:
        """Get last alert for a given key."""
        for alert in reversed(self._alert_history):
            if alert.name == alert_key:
                return alert
        return None

    async def resolve_alert(self, alert_key: str) -> None:
        """Resolve an alert."""
        if alert_key in self._active_alerts:
            alert = self._active_alerts[alert_key]
            alert.state = "resolved"
            alert.last_update = datetime.now()
            self._alert_history.append(alert)
            del self._active_alerts[alert_key]
            self.logger.info(f"Alert resolved: {alert_key}")

    def get_active_alerts(self) -> List[Alert]:
        """Get all active (firing) alerts."""
        return list(self._active_alerts.values())

    def get_alert_history(self, limit: int = 100) -> List[Alert]:
        """Get alert history."""
        return self._alert_history[-limit:]
