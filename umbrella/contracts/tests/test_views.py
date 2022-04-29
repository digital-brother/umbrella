from unittest import mock
from unittest.mock import Mock

import pytest
from django.urls import reverse
from faker import Faker

from umbrella.contracts.models import Contract, Tag
from umbrella.contracts.tests.factories import StartKDPFactory, TaskFactory, ContractFactory, ContractPartyFactory, \
    TagFactory

fake = Faker()
pytestmark = pytest.mark.django_db


def test_contract_list(client, contract):
    url = reverse('contract-list')
    response = client.get(url, format='json')
    assert response.status_code == 200
    assert response.data['count'] == 1
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


def test_kdp_clause_list(client):
    start_kdp = StartKDPFactory()
    kdp_type = "start"
    url = reverse('kdp_clause', args=[start_kdp.contract.id, start_kdp.clause.type])

    response = client.get(url, format='json')

    kdp_data = response.data["results"][0]
    assert kdp_data["id"] == str(start_kdp.id)
    assert kdp_data["type"] == kdp_type
    assert kdp_data["clause"]["id"] == str(start_kdp.clause.id)


@mock.patch('umbrella.contracts.views.load_aws_analytics_jsons_to_db', Mock())
def test_contract_processed_aws_webhook(client, contract):
    url = reverse('contract_processed_aws_webhook', args=[contract.id])
    response = client.post(url)
    assert response.status_code == 200


def test_get_list_with_data_for_document_library(client, contract):
    url = reverse('document_library')
    contractig_party = ContractPartyFactory(contract=contract)
    child_contract = ContractFactory(parent=contract)

    response = client.get(url, format='json')
    data = response.data["results"][0]
    assert response.status_code == 200
    assert data['id'] == str(contract.id)
    assert data['children'][0]['id'] == str(child_contract.id)
    assert data['contracting_parties'][0]['id'] == str(contractig_party.id)




def test_get_statistics_from_contracts_for_document_library(client):
    url = reverse('contracts_statistics')
    ContractFactory()
    TaskFactory()

    response = client.get(url, format='json')
    data = response.data['contracts_statistic']
    assert response.status_code == 200
    assert data['contracts_count'] == 2
    assert data['contracts_with_task_count'] == 1
    assert data['contracts_without_task_count'] == 1
    

def test_create_tag_with_different_type(client, contract):
    url = '/api/v1/contracts/tags/'
    valid_data = {
        "name": "Test",
        "type": "others",
        "contracts": [
            contract.id
        ]
    }
    invalid_data = {
        "name": "Test",
        "type": "nature",
        "contracts": [
            contract.id
        ]
    }
    valid_response = client.post(url, data=valid_data, format='json')
    invalid_response = client.post(url, data=invalid_data, format='json')
    assert valid_response.status_code == 201
    assert invalid_response.status_code == 400
    

def test_update_tag_with_different_type(client, contract):
    url = '/api/v1/contracts/tags/'
    valid_tag = TagFactory()
    invalid_tag = TagFactory(type=Tag.TagTypes.NATURE)
    data = {"name": "Test"}

    valid_response = client.patch(f"{url}{valid_tag.id}/", data=data, format='json')
    invalid_response = client.patch(f"{url}{invalid_tag.id}/", data=data, format='json')
    assert valid_response.status_code == 200
    assert invalid_response.status_code == 400