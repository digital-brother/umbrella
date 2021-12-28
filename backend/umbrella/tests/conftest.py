import pytest
from rest_framework.test import APIClient
from django.conf import settings

@pytest.fixture
def api_client():
    return APIClient
