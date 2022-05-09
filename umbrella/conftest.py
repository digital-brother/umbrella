from urllib.parse import urlencode

import pytest
from django.urls import reverse
from pytest_factoryboy import register
from rest_framework.test import APIClient

from umbrella.contracts.tests.factories import ContractFactory, TagFactory, ContractingPartyFactory
from umbrella.tasks.tests.factories import TaskFactory, CommentFactory
from umbrella.users.tests.factories import UserFactory, GroupFactory

register(GroupFactory)
register(TagFactory)
register(ContractingPartyFactory)
register(CommentFactory)


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_login(user)
    return client


@pytest.fixture
def user(group):
    return UserFactory(groups=[group])


@pytest.fixture
def contract(group, node):
    return ContractFactory(groups=[group], clauses=[node])


def contract_with_tag(group, node, tag):
    return ContractFactory(groups=[group], clauses=[node], tags=[tag])


@pytest.fixture
def parent_contract(contract):
    child_contract = ContractFactory()
    contract.children.add(child_contract)
    return contract


@pytest.fixture
def task(user):
    return TaskFactory(assignees=[user])


def reverse_with_params(viewname, args=None, kwargs=None, query_kwargs=None):
    """
    Custom reverse to add a query string after the url
    Example usage:
    url = my_reverse('my_test_url', kwargs={'pk': object.id}, query_kwargs={'next': reverse('home')})
    """
    url = reverse(viewname, args=args, kwargs=kwargs)

    if query_kwargs:
        return f'{url}?{urlencode(query_kwargs)}'

    return url
