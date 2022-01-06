"""This file is used for testing 'lease' model CRUD API."""
import json

import pytest
from umbrella.models.lease import Lease


@pytest.mark.django_db
class TestLeaseApiEndpoints:
    """This Class is used to test 'lease' api CRUD."""

    ENDPOINT = "/umbrella/lease/"
    ID = 1
    test_file_name = "test-file"

    CREATE_JSON = {
        "id": ID,
        "file_name": "test-file",
        "pdf": None,
        "txt": "test-txt",
        "extracted": "test-extracted",
        "address": "test-address",
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
        "doc_type": "",
    }

    UPDATE_FILE_NAME = "udpated-file-name"
    UPDATE_JSON = {
        "id": ID,
        "file_name": "udpated-file-name",
        "pdf": None,
        "txt": "test-txt",
        "extracted": "test-extracted",
        "address": "test-address",
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
        "doc_type": "",
    }

    def test_list(self, api_client):
        """This function is used to test 'lease' api getAll."""
        response = api_client().get(self.ENDPOINT)
        assert response.status_code == 200

    def test_create(self, api_client):
        """This function is used to test 'lease' api create."""
        create_response = api_client().post(
            self.ENDPOINT, data=self.CREATE_JSON, format="json"
        )

        assert create_response.status_code == 201
        assert json.loads(create_response.content) == self.CREATE_JSON

    def test_delete(self, api_client):
        """This function is used to test 'lease' api delete."""
        create_test_lease = Lease(id=self.ID, file_name=self.test_file_name)
        create_test_lease.save()

        delete_url = f"{self.ENDPOINT}{create_test_lease.id}/"
        delete_response = api_client().delete(delete_url)

        assert delete_response.status_code == 204

    def test_update(self, api_client):
        """This function is used to test 'lease' api update."""
        create_test_lease = Lease(id=self.ID, file_name=self.test_file_name)
        create_test_lease.save()

        update_url = f"{self.ENDPOINT}{create_test_lease.id}/"
        update_response = api_client().put(
            update_url, data=self.UPDATE_JSON, format="json"
        )

        assert update_response.status_code == 200
        assert json.loads(update_response.content) == self.UPDATE_JSON
