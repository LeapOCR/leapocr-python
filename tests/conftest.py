"""
Test configuration and utilities for LeapOCR Python SDK tests.
"""

from unittest.mock import Mock

import pytest

from leapocr import LeapOCRClient


@pytest.fixture
def api_key():
    """Fixture providing a test API key."""
    return "test_api_key_123456789"


@pytest.fixture
def client(api_key):
    """Fixture providing a configured LeapOCR client."""
    return LeapOCRClient(api_key=api_key)


@pytest.fixture
def mock_gen_client():
    """Fixture providing a mock generated client."""
    return Mock()


@pytest.fixture
def sample_job_response():
    """Fixture providing sample job response data."""
    return {
        "job_id": "test_job_123",
        "status": "pending",
        "created_at": "2023-12-25T10:30:00Z",
    }


@pytest.fixture
def sample_job_result():
    """Fixture providing sample job result data."""
    return {
        "job_id": "test_job_123",
        "status": "completed",
        "data": {"extracted_text": "Sample text content"},
        "credits_used": 10,
        "processing_time": 5.2,
        "created_at": "2023-12-25T10:30:00Z",
        "completed_at": "2023-12-25T10:35:12Z",
    }


@pytest.fixture
def sample_upload_response():
    """Fixture providing sample upload response data."""
    return {
        "job_id": "upload_job_123",
        "upload_url": "https://upload.example.com/presigned",
        "headers": {"Content-Type": "application/pdf"},
    }


@pytest.fixture
def sample_api_error():
    """Fixture providing sample API error."""
    from leapocr.gen.openapi_client.exceptions import ApiException

    return ApiException(status=400, reason="Bad Request")


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow")
    config.addinivalue_line("markers", "asyncio: mark test as async")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers."""
    for item in items:
        # Mark integration tests
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)

        # Mark slow tests
        if "slow" in item.nodeid or "wait_for" in item.nodeid:
            item.add_marker(pytest.mark.slow)

        # Mark async tests
        if "async" in item.nodeid:
            item.add_marker(pytest.mark.asyncio)
