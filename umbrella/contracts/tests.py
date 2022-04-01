import pytest
from django.urls import reverse
from pytest_factoryboy import register
from rest_framework.test import APIClient

from umbrella.users.test.factories import UserFactory

register(UserFactory)


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_login(user)
    return client


@pytest.mark.django_db
def test_lease_list(client):
    url = reverse('lease-list')
    response = client.get(url, format='json')
    assert response.status_code == 200
