import pytest
from django.contrib.auth.models import Group
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from rest_framework.test import APIClient

from umbrella.tests.test_contracts import LeaseFactory
from umbrella.users.test.factories import UserFactory


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_login(user)
    return client


@pytest.fixture
def user(group):
    user = UserFactory(groups=[group])
    return user


@register
class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = 'no_group'


@pytest.fixture
def lease(group):
    lease = LeaseFactory(groups=[group])
    return lease
