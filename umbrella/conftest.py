import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from umbrella.contracts.tests.factories import ContractFactory, TagFactory, ContractingPartyFactory
from umbrella.users.tests.factories import UserFactory, GroupFactory

register(GroupFactory)
register(TagFactory)
register(ContractingPartyFactory)


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_login(user)
    return client


@pytest.fixture
def user(group):
    user = UserFactory(groups=[group])
    return user


@pytest.fixture
def contract(group, node, tag):
    contract = ContractFactory(groups=[group], clauses=node, tags=[tag])
    return contract
