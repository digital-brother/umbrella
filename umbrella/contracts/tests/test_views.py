from unittest import mock
from unittest.mock import Mock

import pytest
from django.urls import reverse
from faker import Faker

from umbrella.contracts.models import Contract, Tag
from umbrella.contracts.tests.factories import StartKDPFactory, TaskFactory, TagFactory

fake = Faker()
pytestmark = pytest.mark.django_db


def test_contract_list(client, contract):
    url = reverse('contract-list')
    response = client.get(url, format='json')
    assert response.status_code == 200
    assert response.data['count'] == 1
    contract_data = response.data['results'][0]
    assert contract_data['id'] == str(contract.id)


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


def test_document_library(client, parent_contract):
    url = reverse('document_library')
    response = client.get(url, format='json')
    parent_contract_data = response.data["results"][0]

    assert response.status_code == 200
    assert parent_contract_data['id'] == str(parent_contract.id)

    child_contract_data = parent_contract_data['children'][0]
    child_contract = parent_contract.children.first()
    assert child_contract_data['id'] == str(child_contract.id)

    parent_contract_contracting_party = parent_contract.contracting_parties.last()
    parent_contract_contracting_parties_data = parent_contract_data['contracting_parties'][0]
    assert parent_contract_contracting_parties_data['id'] == str(parent_contract_contracting_party.id)


def test_contracts_statistics(client, contract):
    url = reverse('contracts_statistics')
    TaskFactory()

    response = client.get(url, format='json')
    assert response.status_code == 200

    data = response.data['contracts_statistic']
    assert data['contracts_count'] == 2
    assert data['contracts_with_task_count'] == 1
    assert data['contracts_without_task_count'] == 1


def test_tag_list(client, tag):
    url = reverse('tag-list')
    response = client.get(url, format='json')

    assert response.status_code == 200
    assert response.data['count'] == 1


def test__create_tag__with_others_type(client, contract):
    url = reverse('tag-list')
    tag_name = 'created_test_others_tag'
    data = {
        "name": tag_name,
        "type": "others",
        "contracts": [
            contract.id
        ]
    }
    response = client.post(url, data=data, format='json')
    assert response.status_code == 201
    assert response.data['name'] == tag_name
    assert Tag.objects.count() == 1


def test__create_tag__with_nature_type(client, contract):
    url = reverse('tag-list')
    data = {
        "name": "created_test_nature_tag",
        "type": "nature",
        "contracts": [
            contract.id
        ]
    }
    response = client.post(url, data=data, format='json')
    assert response.status_code == 400
    assert response.data['non_field_errors'][0] == 'Only Others tag can be created'


def test__update_tag__with_others_type(client, tag):
    new_tag_name = 'updated_test_others_tag'
    data = {"name": new_tag_name}
    url = reverse('tag-detail', args=[tag.id])

    response = client.patch(url, data=data, format='json')
    assert response.status_code == 200
    assert response.data['name'] == new_tag_name


def test__update_tag__with_nature_type(client, contract):
    tag = TagFactory(type=Tag.TagTypes.NATURE)
    data = {"name": "updated_test_nature_tag"}
    url = reverse('tag-detail', args=[tag.id])
    response = client.patch(url, data=data, format='json')
    assert response.status_code == 400


def test__delete_tag__with_others_type(client, tag):
    url = reverse('tag-detail', args=[tag.id])
    response = client.delete(url, format='json')
    assert response.status_code == 204
    assert Tag.objects.count() == 0


def test__delete_tag__with_nature_type(client, contract):
    tag = TagFactory(type=Tag.TagTypes.NATURE)
    url = reverse('tag-detail', args=[tag.id])
    response = client.delete(url, format='json')
    assert response.status_code == 400
    assert response.data[0] == "You are not allowed to delete Tag with type 'nature'."
