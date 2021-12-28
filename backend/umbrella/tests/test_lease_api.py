import json
import pytest
from umbrella.models.Lease import Lease
from django.db.models import Model, NOT_PROVIDED, DateTimeField
from datetime import datetime

@pytest.mark.django_db
class TestLeaseApiEndpoints:

    ENDPOINT = '/umbrella/lease/'
    ID = 1
    TEST_FILE_NAME = "test-file"
    TEST_TXT = "test-txt"
    TEST_EXTRACTED = "test-extracted"
    TEST_ADDRESS = "test-address"

    CREATE_JSON = {
        "id": ID,
        "file_name": TEST_FILE_NAME,
        "pdf": None,
        "txt": TEST_TXT,
        "extracted": TEST_EXTRACTED,
        "address": TEST_ADDRESS,
        "createdon": "2021-12-17T00:30:00Z",
        "createdby": "test-user",
        "modifiedon": "2021-12-17T00:30:00Z",
        "modifiedby": "test-user",
        "activeflag": True,
        "contract_type": "test",
        "textract": "",
        "analyticsdata": "",
        "pdf_hash": "",
        "file_size": 10,
        "modified_file_name": "",
        "analytics2": "",
        "doc_type": ""
    }

    UPDATE_FILE_NAME = "udpated-file-name"
    UPDATE_JSON = {
        "id": ID,
        "file_name": UPDATE_FILE_NAME,
        "pdf": None,
        "txt": TEST_TXT,
        "extracted": TEST_EXTRACTED,
        "address": TEST_ADDRESS,
        "createdon": "2021-12-17T00:30:00Z",
        "createdby": "test-user",
        "modifiedon": "2021-12-17T00:30:00Z",
        "modifiedby": "test-user",
        "activeflag": False,
        "contract_type": "test",
        "textract": "",
        "analyticsdata": "",
        "pdf_hash": "",
        "file_size": 10,
        "modified_file_name": "",
        "analytics2": "",
        "doc_type": ""
    }

    def test_list(self, api_client):
        response = api_client().get(self.ENDPOINT)
        assert response.status_code == 200

    def test_create(self, api_client):
        create_response = api_client().post(self.ENDPOINT, data=self.CREATE_JSON, format='json')

        assert create_response.status_code == 201
        assert json.loads(create_response.content) == self.CREATE_JSON
        assert Lease.objects.count() == 1

    def test_delete(self, api_client):
        create_test_lease = Lease.objects.create(id=self.ID, file_name=self.TEST_FILE_NAME)
        assert Lease.objects.count() == 1

        delete_url = f'{self.ENDPOINT}{create_test_lease.id}/'
        delete_response = api_client().delete(delete_url)

        assert delete_response.status_code == 204
        assert Lease.objects.count() == 0

  
    def test_update(self, api_client):
        create_test_lease = Lease.objects.create(id=self.ID, file_name=self.TEST_FILE_NAME)
        assert Lease.objects.count() == 1

        update_url = f'{self.ENDPOINT}{create_test_lease.id}/'
        update_response = api_client().put(update_url, data=self.UPDATE_JSON, format='json')

        assert update_response.status_code == 200
        assert Lease.objects.count() == 1
        assert json.loads(update_response.content) == self.UPDATE_JSON