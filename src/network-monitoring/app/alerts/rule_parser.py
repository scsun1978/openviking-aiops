"""
Rule parser module - Parse alert rules from YAML/JSON configuration
"""

import yaml
import json
import logging
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class ThresholdCondition:
    """Threshold condition for alert rules."""
    metric: str
    operator: str  # >, <, =, !=, >=, <=
    threshold: float
    duration: int  # seconds


@dataclass
class TrendCondition:
    """Trend condition for alert rules."""
    metric: str
    type: str  # growth, decline
    rate: float  # percentage
    duration: int  # seconds


@dataclass
class AlertRule:
    """Alert rule definition."""
    name: str
    enabled: bool
    conditions: List[ThresholdCondition | TrendCondition]
    aggregator: str  # AND, OR
    severity: str  # info, warning, critical
    message: str
    labels: Dict[str, str]
    suppress_duration: int  # seconds
    group_by: List[str]


class RuleParser:
    """Parse alert rules from configuration files."""

    def __init__(self):
        """Initialize rule parser."""
        self.logger = logging.getLogger(__name__)

    def parse_from_yaml(self, yaml_content: str) -> List[AlertRule]:
        """Parse alert rules from YAML content."""
        try:
            data = yaml.safe_load(yaml_content)
            return self._parse_rules(data)
        except yaml.YAMLError as e:
            self.logger.error(f"Failed to parse YAML: {e}")
            return []

    def parse_from_json(self, json_content: str) -> List[AlertRule]:
        """Parse alert rules from JSON content."""
        try:
            data = json.loads(json_content)
            return self._parse_rules(data)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON: {e}")
            return []

    def _parse_rules(self, data: Dict[str, Any]) -> List[AlertRule]:
        """Parse rules from parsed data."""
        rules = []

        if not data or "rules" not in data:
            self.logger.warning("No rules found in configuration")
            return []

        for rule_data in data["rules"]:
            try:
                rule = AlertRule(
                    name=rule_data.get("name", "unnamed"),
                    enabled=rule_data.get("enabled", True),
                    conditions=self._parse_conditions(rule_data.get("conditions", [])),
                    aggregator=rule_data.get("aggregator", "AND"),
                    severity=rule_data.get("severity", "warning"),
                    message=rule_data.get("message", ""),
                    labels=rule_data.get("labels", {}),
                    suppress_duration=rule_data.get("suppress_duration", 0),
                    group_by=rule_data.get("group_by", [])
                )
                rules.append(rule)
                self.logger.info(f"Parsed rule: {rule.name}")
            except Exception as e:
                self.logger.error(f"Failed to parse rule: {e}")

        return rules

    def _parse_conditions(self, conditions_data: List[Dict[str, Any]]) -> List[ThresholdCondition | TrendCondition]:
        """Parse conditions from data."""
        conditions = []

        for condition_data in conditions_data:
            try:
                if "threshold" in condition_data:
                    # Threshold condition
                    condition = ThresholdCondition(
                        metric=condition_data.get("metric", ""),
                        operator=condition_data.get("operator", ">"),
                        threshold=float(condition_data.get("threshold", 0)),
                        duration=condition_data.get("duration", 0)
                    )
                    conditions.append(condition)
                elif "trend" in condition_data:
                    # Trend condition
                    condition = TrendCondition(
                        metric=condition_data.get("metric", ""),
                        type=condition_data.get("type", "growth"),
                        rate=float(condition_data.get("rate", 0)),
                        duration=condition_data.get("duration", 0)
                    )
                    conditions.append(condition)
            except Exception as e:
                self.logger.error(f"Failed to parse condition: {e}")

        return conditions
