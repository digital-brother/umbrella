import factory
import pytest
from django.contrib.auth.models import Group
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from rest_framework.test import APIClient

from umbrella.contracts.models import Node, Tag
from umbrella.contracts.tests.factories import ContractFactory
from umbrella.users.tests.factories import UserFactory


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


@register
class NodeFactory(DjangoModelFactory):
    type = "contractingParties"

    class Meta:
        model = Node


@register
class TagFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"task_{n}")
    type = Tag.TagTypes.OTHERS

    class Meta:
        model = Tag


@pytest.fixture
def contract(group, node, tag):
    contract = ContractFactory(groups=[group], clauses=node, tags=[tag])
    return contract


@pytest.fixture
def parent_contract(contract, group):
    parent_contract = ContractFactory(groups=[group])
    parent_contract.children.add(contract)
    return parent_contract