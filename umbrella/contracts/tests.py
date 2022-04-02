import factory
import pytest
from django.urls import reverse
from factory.django import DjangoModelFactory

from umbrella.contracts.models import Lease
from umbrella.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_lease_list(client, lease):
    url = reverse('lease-list')
    response = client.get(url, format='json')
    assert response.status_code == 200
    assert response.data['count']
    assert response.data['results'][0]['uuid'] == str(lease.uuid)


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
