from unittest import mock
from unittest.mock import Mock

import factory
import pytest
from django.urls import reverse
from factory.django import DjangoModelFactory

from umbrella.contracts.models import Lease
from umbrella.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test__lease_list(client, lease):
    url = reverse('lease-list')
    response = client.get(url, format='json')
    assert response.status_code == 200
    assert response.data['count']
    response_lease_data = response.data['results'][0]
    assert response_lease_data['id'] == str(lease.id)


@mock.patch('umbrella.contracts.views.create_presigned_post', Mock(return_value={}))
def test__lease_create(client):
    url = reverse('lease-create')
    data = {
        "file_name": "contract.pdf",
        "file_size": 1024,
        "file_hash": "contract_hash"
    }
    response = client.post(url, data=data, format='json')
    assert response.status_code == 200
    assert Lease.objects.count() == 1


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
