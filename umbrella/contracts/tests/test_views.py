from unittest import mock
from unittest.mock import Mock

import pytest
from django.urls import reverse
from faker import Faker

from umbrella.contracts.models import Contract
from umbrella.contracts.tests.factories import NodeFactory

fake = Faker()
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


def test_kdp_with_clause_list(client, contract, node):
    kdp_type = "start"
    NodeFactory(type=kdp_type, clause=node, contract=None)
    url = reverse('kdp_clause', args=[contract.id, node.type])
    response = client.get(url, format='json')
    assert response.data["count"] == 1
    assert response.data["results"][0]["type"] == kdp_type
