from urllib.parse import urlencode

import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from rest_framework.test import APIClient

from umbrella.contracts.tests.factories import ContractFactory
from umbrella.tasks.tests.factories import TaskFactory
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


@pytest.fixture
def contract(group):
    contract = ContractFactory(groups=[group])
    return contract


@pytest.fixture
def task(user):
    task = TaskFactory(assignees=[user])
    return task


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
