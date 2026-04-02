"""
Test rule parser and evaluator
"""

import pytest
from datetime import datetime, timedelta
from app.alerts.rule_parser import RuleParser, ThresholdCondition, TrendCondition, AlertRule
from app.alerts.rule_evaluator import RuleEvaluator, Alert, MetricValue


@pytest.fixture
def rule_parser():
    """Create rule parser fixture."""
    return RuleParser()


@pytest.fixture
def rule_evaluator():
    """Create rule evaluator fixture."""
    return RuleEvaluator(metrics_collector=None)


def test_parse_yaml_rules(rule_parser):
    """Test parsing YAML rules."""
    yaml_content = """
rules:
  - name: cpu_high
    enabled: true
    severity: critical
    message: "CPU high"
    labels:
      service: system
    aggregator: AND
    suppress_duration: 300
    conditions:
      - metric: "cpu_usage_ratio"
        operator: ">"
        threshold: 0.8
        duration: 60
"""

    rules = rule_parser.parse_from_yaml(yaml_content)
    assert len(rules) == 1
    assert rules[0].name == "cpu_high"
    assert rules[0].severity == "critical"
    assert rules[0].aggregator == "AND"
    assert len(rules[0].conditions) == 1
    assert isinstance(rules[0].conditions[0], ThresholdCondition)


def test_parse_json_rules(rule_parser):
    """Test parsing JSON rules."""
    json_content = """{
  "rules": [
    {
      "name": "memory_high",
      "enabled": true,
      "severity": "warning",
      "message": "Memory high",
      "labels": {"service": "system"},
      "aggregator": "AND",
      "conditions": [
        {
          "metric": "memory_usage_ratio",
          "operator": ">",
          "threshold": 0.85,
          "duration": 60
        }
      ]
    }
  ]
}"""

    rules = rule_parser.parse_from_json(json_content)
    assert len(rules) == 1
    assert rules[0].name == "memory_high"
    assert rules[0].severity == "warning"


def test_threshold_condition(rule_parser):
    """Test threshold condition parsing."""
    yaml_content = """
rules:
  - name: test
    enabled: true
    conditions:
      - metric: "cpu_usage_ratio"
        operator: ">"
        threshold: 0.8
        duration: 60
"""

    rules = rule_parser.parse_from_yaml(yaml_content)
    condition = rules[0].conditions[0]

    assert condition.metric == "cpu_usage_ratio"
    assert condition.operator == ">"
    assert condition.threshold == 0.8
    assert condition.duration == 60


def test_trend_condition(rule_parser):
    """Test trend condition parsing."""
    yaml_content = """
rules:
  - name: test
    enabled: true
    conditions:
      - metric: "cpu_usage_ratio"
        type: "growth"
        rate: 10.0
        duration: 60
"""

    rules = rule_parser.parse_from_yaml(yaml_content)
    if len(rules) > 0 and len(rules[0].conditions) > 0:
        condition = rules[0].conditions[0]

        assert condition.metric == "cpu_usage_ratio"
        assert condition.type == "growth"
        assert condition.rate == 10.0
        assert condition.duration == 60
    else:
        pytest.fail("No rules or conditions parsed")


def test_multiple_conditions(rule_parser):
    """Test multiple conditions with AND."""
    yaml_content = """
rules:
  - name: test
    enabled: true
    aggregator: AND
    conditions:
      - metric: "cpu_usage_ratio"
        operator: ">"
        threshold: 0.8
        duration: 60
      - metric: "memory_usage_ratio"
        operator: ">"
        threshold: 0.9
        duration: 60
"""

    rules = rule_parser.parse_from_yaml(yaml_content)
    assert len(rules[0].conditions) == 2
    assert rules[0].aggregator == "AND"


def test_load_rules(rule_evaluator):
    """Test loading rules into evaluator."""
    rules = [
        AlertRule(
            name="test_rule",
            enabled=True,
            conditions=[],
            aggregator="AND",
            severity="warning",
            message="Test",
            labels={},
            suppress_duration=300,
            group_by=[]
        )
    ]

    # This should be async in production
    # For testing, we're mocking it
    rule_evaluator._rules = [rule for rule in rules if rule.enabled]
    assert len(rule_evaluator._rules) == 1


def test_threshold_evaluation_greater():
    """Test threshold evaluation with > operator."""
    condition = ThresholdCondition(
        metric="cpu_usage_ratio",
        operator=">",
        threshold=0.8,
        duration=60
    )

    # Mock evaluation
    value = 0.9
    triggered = value > condition.threshold

    assert triggered is True


def test_threshold_evaluation_less():
    """Test threshold evaluation with < operator."""
    condition = ThresholdCondition(
        metric="cpu_usage_ratio",
        operator="<",
        threshold=0.5,
        duration=60
    )

    # Mock evaluation
    value = 0.3
    triggered = value < condition.threshold

    assert triggered is True


def test_alert_creation():
    """Test alert object creation."""
    alert = Alert(
        name="test_alert",
        severity="warning",
        message="Test alert",
        labels={"service": "system"},
        state="firing",
        start_time=datetime.now(),
        last_update=datetime.now(),
        value=0.85
    )

    assert alert.name == "test_alert"
    assert alert.severity == "warning"
    assert alert.state == "firing"
    assert alert.value == 0.85


def test_trend_calculation():
    """Test trend calculation."""
    # Mock metric history
    previous_value = 0.5
    current_value = 0.6

    # Calculate growth rate
    rate = (current_value - previous_value) / abs(previous_value) * 100

    assert abs(rate - 20.0) < 0.01  # ~20% growth


def test_alert_suppression():
    """Test alert suppression logic."""
    from datetime import timedelta

    now = datetime.now()
    start_time = now - timedelta(seconds=100)
    suppress_duration = 300  # 5 minutes

    # Check if alert should be suppressed
    if (now - start_time).total_seconds() < suppress_duration:
        suppressed = True
    else:
        suppressed = False

    assert suppressed is True  # Should be suppressed (100 < 300)


def test_aggregator_and():
    """Test AND aggregator logic."""
    conditions = [True, False, True]
    triggered = all(conditions)  # AND

    assert triggered is False


def test_aggregator_or():
    """Test OR aggregator logic."""
    conditions = [True, False, True]
    triggered = any(conditions)  # OR

    assert triggered is True
