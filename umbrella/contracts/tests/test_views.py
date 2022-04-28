from unittest import mock
from unittest.mock import Mock

import pytest
from django.urls import reverse
from faker import Faker, factory

from umbrella.contracts.models import Contract, Node, Tag
from umbrella.contracts.tests.factories import StartKDPFactory, TaskFactory, ContractFactory, ContractPartyFactory
from umbrella.users.tests.factories import UserFactory

fake = Faker()
pytestmark = pytest.mark.django_db


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


def test_get_list_with_data_for_document_library(client):
    user = UserFactory()
    contract = ContractFactory(created_by=user)
    [contract.groups.add(group) for group in user.groups.all()]
    client.force_authenticate(user)
    response = client.get(reverse('document_library'))
    data = response.data['results']
    dict_data = dict((key, value) for (key, value) in data[0].items())
    assert dict_data['file_name'] == contract.file_name
    assert len(data) == 1
    assert response.status_code == 200


def test_get_statistics_from_contracts_for_document_library(client):
    contract = ContractFactory()
    task = TaskFactory()
    response = client.get(reverse('contracts_statistics'))
    data = response.data['contracts_statistic']
    assert response.status_code == 200
    assert data['contracts_count'] == 2
    assert data['contracts_with_task_count'] == 1
    assert data['contracts_without_task_count'] == 1




