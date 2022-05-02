from unittest import mock
from unittest.mock import Mock

import pytest
from django.urls import reverse
from faker import Faker

from umbrella.conftest import TagFactory
from umbrella.contracts.models import Contract, Tag, Node
from umbrella.contracts.tests.factories import StartKDPFactory, TaskFactory, ContractFactory

fake = Faker()
pytestmark = pytest.mark.django_db


def test_contract_list(client, contract):
    url = reverse('contract-list')
    response = client.get(url, format='json')
    assert response.status_code == 200
    assert response.data['count'] == 2
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


def test_document_library(client, contract):
    url = reverse('document_library')
    related_contracting_party = contract.clauses.filter(type='contractingParties').last()

    response = client.get(url, format='json')
    contract_parent_data = response.data["results"][0]

    assert response.status_code == 200
    assert contract_parent_data['id'] == str(contract.parent_id)
    contract_data = contract_parent_data['children'][0]
    assert contract_data['id'] == str(contract.id)
    assert contract_data['contracting_parties'][0]['id'] == str(related_contracting_party.id)


def test_contracts_statistics(client, contract):
    url = reverse('contracts_statistics')
    TaskFactory()

    response = client.get(url, format='json')
    data = response.data['contracts_statistic']
    assert response.status_code == 200
    assert data['contracts_count'] == 4
    assert data['contracts_with_task_count'] == 1
    assert data['contracts_without_task_count'] == 3


def test_tag_list(client, contract):
    url = reverse('tag-list')
    response = client.get(url, format='json')
    related_tags_ids = contract.tags.all().values_list('id', flat=True)

    assert response.status_code == 200
    assert response.data['count'] == 1
    tag_data = response.data["results"][0]
    assert tag_data['id'] in str(related_tags_ids)
    assert tag_data['contracts'][0] == contract.id


def test_create_tag_with_others_type(client, contract):
    url = reverse('tag-list')
    data = {
        "name": "Test",
        "type": "others",
        "contracts": [
            contract.id
        ]
    }
    response = client.post(url, data=data, format='json')
    assert response.status_code == 201


def test_create_tag_with_nature_type(client, contract):
    url = reverse('tag-list')
    data = {
        "name": "Test",
        "type": "nature",
        "contracts": [
            contract.id
        ]
    }
    response = client.post(url, data=data, format='json')
    assert response.status_code == 400


def test_update_tag_with_others_type(client, contract):
    tag = TagFactory()
    data = {"name": "Test"}
    url = reverse('tag-detail', args=[tag.id])

    response = client.patch(url, data=data, format='json')
    assert response.status_code == 200


def test_update_tag_with_nature_type(client, contract):
    tag = TagFactory(type=Tag.TagTypes.NATURE)
    data = {"name": "Test"}
    url = reverse('tag-detail', args=[tag.id])

    response = client.patch(url, data=data, format='json')
    assert response.status_code == 400


def test_delete_tag_with_others_type(client, contract):
    tag = TagFactory()
    url = reverse('tag-detail', args=[tag.id])

    response = client.delete(url, format='json')
    assert response.status_code == 204


def test_delete_tag_with_nature_type(client, contract):
    tag = TagFactory(type=Tag.TagTypes.NATURE)
    url = reverse('tag-detail', args=[tag.id])

    response = client.delete(url, format='json')
    assert response.status_code == 400
