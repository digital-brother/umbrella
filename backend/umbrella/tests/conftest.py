"""We can define the fixture functions in this file
to make them accessible across multiple test files."""
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Run before the test function is executed to get API Client."""
    return APIClient
