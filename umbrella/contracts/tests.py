import factory
import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from rest_framework.test import APIClient

from umbrella.contracts.models import Lease
from umbrella.users.test.factories import UserFactory


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = 'no_group'


register(GroupFactory)


@pytest.fixture
def user(group):
    user = UserFactory(groups=[group])
    return user


class LeaseFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    file_size = 1024

    class Meta:
        model = Lease

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for extracted_group in extracted:
                self.groups.add(extracted_group)


@pytest.fixture
def lease(group):
    lease = LeaseFactory(groups=[group])
    return lease


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_login(user)
    return client


@pytest.mark.django_db
def test_lease_list(client, lease):
    url = reverse('lease-list')
    response = client.get(url, format='json')
    assert response.status_code == 200
    assert response.data['count']
    assert response.data['results'][0]['uuid'] == str(lease.uuid)
