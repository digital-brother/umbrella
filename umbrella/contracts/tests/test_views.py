from unittest import mock
from unittest.mock import Mock

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase, APIClient

from umbrella.contracts.models import Contract, Node, Tag
from umbrella.contracts.tests.factories import StartKDPFactory
from umbrella.tasks.models import Task
from umbrella.users.auth import User

fake = Faker()
pytestmark = pytest.mark.django_db


TEST_CONTRACT_FILES_DIR = "umbrella/contracts/test_analytics_jsons/6cb7fa02-457f-4e91-be84-3bfea7692d6b"
TEST_CONTRACT_UUID = TEST_CONTRACT_FILES_DIR.split('/')[-1]


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


def test_document_library_list(client, contract):
    url = reverse('document_library')
    response = client.get(url, format='json')
    assert response.status_code == 200
    print(response.data)
    assert response.data['count']
    response_contract_data = response.data['results'][0]
    assert response_contract_data['id'] == str(contract.id)



class TestDocumentLibraryTestCase(APITestCase):


    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='Test', password='test')

        self.contract_1 = Contract.objects.create(file_name="Test1.pdf", created_by=self.user, file_hash="TestTest1",
                                                  file_size=25464,
                                                  modified_file_name="651415F6-8396-9090-1869-50ACF85AC196.pdf")
        self.contract_2 = Contract.objects.create(file_name="Test2.pdf", created_by=self.user, file_hash="TestTest2",
                                                  file_size=25464, parent=self.contract_1,
                                                  modified_file_name="979803EB-2DBE-6203-6B85-2329A19AF847.pdf")
        self.contract_party = Node.objects.create(type='contractingParties',
                                                  contract=self.contract_1, content="test")
        self.contract_start = Node.objects.create(type='start', contract=self.contract_1, content="test")
        self.contract_type = Node.objects.create(type='contractType', contract=self.contract_2, content="test")
        self.tag = Tag.objects.create(name="Test1", type=Tag.TagTypes.NATURE)
        self.tag.contracts.add(self.contract_2)
        self.task = Task.objects.create(title="Test1", contract_clause_type="test", contract=self.contract_2,
                                        contract_business_intelligence_type="test", link_to_contract_text='test')


    def test_get_list_with_data_for_document_library(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/api/v1/contracts/document-library/')
        self.assertEqual(200, response.status_code)

    def test_get_statistics_from_contracts_for_document_library(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/api/v1/contracts/contracts-statistics/')
        data = response.data['contracts_statistic']
        self.assertEqual(Contract.objects.all().count(), data['contracts_count'])
        self.assertEqual(Contract.objects.filter(tasks__isnull=False).count(), data['contracts_with_task_count'])
        self.assertEqual(200, response.status_code)


