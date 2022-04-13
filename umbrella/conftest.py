import pytest
from django.contrib.auth.models import Group
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from rest_framework.test import APIClient

from umbrella.contracts.tests.factories import ContractFactory, TermNodeFactory
from umbrella.users.tests.factories import UserFactory


register(UserFactory)
register(ContractFactory)
register(TermNodeFactory)


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
def contract(group):
    contract = ContractFactory(groups=[group])
    return contract
