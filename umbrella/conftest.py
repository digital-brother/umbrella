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
def contract(group, node):
    return ContractFactory(groups=[group], clauses=node)


def contract_with_tag(group, node, tag):
    return ContractFactory(groups=[group], clauses=node, tags=[tag])


@pytest.fixture
def parent_contract(contract):
    child_contract = ContractFactory()
    contract.children.add(child_contract)
    return contract
