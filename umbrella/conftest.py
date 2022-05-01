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
class ContractPartyFactory(DjangoModelFactory):
    type = "contractingParties"

    class Meta:
        model = Node


@register
class TagFactory(DjangoModelFactory):
    name = 'test_tag'
    type = Tag.TagTypes.OTHERS

    class Meta:
        model = Tag


@pytest.fixture
def contract(group, node, tag):
    contract = ContractFactory(groups=[group], clauses=node, tags=[tag])
    return contract
