from unittest import mock
from unittest.mock import Mock

import factory
import pytest
from django.core.management import call_command
from django.urls import reverse
from factory.django import DjangoModelFactory
from uuid import UUID

from pytest_factoryboy import register

from umbrella.contracts.models import Contract, Node
from umbrella.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


TEST_CONTRACT_FILES_DIR = "umbrella/contracts/test_analytics_jsons/6cb7fa02-457f-4e91-be84-3bfea7692d6b"
TEST_CONTRACT_UUID = "6cb7fa02-457f-4e91-be84-3bfea7692d6b"


def test_contract_list(client, contract):
    url = reverse('contract-list')
    response = client.get(url, format='json')
    assert response.status_code == 200
    assert response.data['count']
    response_contract_data = response.data['results'][0]
    assert response_contract_data['id'] == str(contract.id)


@mock.patch('umbrella.contracts.views.create_presigned_post', Mock(return_value={}))
def test_contract_create(client):
    url = reverse('contract-create')
    data = {
        "file_name": "contract.pdf",
        "file_size": 1024,
        "file_hash": "contract_hash"
    }
    response = client.post(url, data=data, format='json')
    assert response.status_code == 200
    assert Contract.objects.count() == 1


def test_parse_contract(client):
    ContractFactory(id=UUID(TEST_CONTRACT_UUID))
    assert Node.objects.count() == 0
    call_command('parse_contract', TEST_CONTRACT_FILES_DIR)
    assert Contract.objects.count() > 0


def test_kdp_with_clause_list(client, contract, node):
    kdp_type = "start"
    NodeFactory(type=kdp_type, clause=node, contract=None)
    url = reverse('kdp_clause', args=[contract.id, node.type])
    response = client.get(url, format='json')
    assert response.data["count"] == 1
    assert response.data["results"][0]["type"] == kdp_type


class ContractFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    file_size = 1024

    class Meta:
        model = Contract

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for extracted_group in extracted:
                self.groups.add(extracted_group)


class NodeFactory(DjangoModelFactory):
    type = "term"
    contract = factory.SubFactory(ContractFactory)

    class Meta:
        model = Node
