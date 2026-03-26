"""
Test fixtures and configuration
"""

import pytest
from prometheus_client import CollectorRegistry


@pytest.fixture
def prometheus_registry():
    """Create a clean Prometheus registry for testing."""
    # Create a new registry instance for each test
    registry = CollectorRegistry()
    return registry


@pytest.fixture
def mock_metrics_collector(prometheus_registry):
    """Create a mock metrics collector for testing."""
    class MockMetricsCollector:
        async def start(self):
            pass
        
        async def stop(self):
            pass
    
    return MockMetricsCollector()
