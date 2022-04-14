import pytest
from django.core.management import call_command
from uuid import UUID

from umbrella.contracts.models import Contract, Node
from umbrella.contracts.tests.factories import ContractFactory

pytestmark = pytest.mark.django_db

TEST_CONTRACT_FILES_DIR = "umbrella/contracts/test_analytics_jsons/6cb7fa02-457f-4e91-be84-3bfea7692d6b"
TEST_CONTRACT_UUID = "6cb7fa02-457f-4e91-be84-3bfea7692d6b"
TEST_KDP_TYPE = "start"


def test_parse_contract(client):
    ContractFactory(id=UUID(TEST_CONTRACT_UUID))
    assert Node.objects.count() == 0
    call_command('parse_contract', TEST_CONTRACT_FILES_DIR)
    assert Contract.objects.count() > 0
    start_kdp = Node.objects.filter(type=TEST_KDP_TYPE).first()
    assert start_kdp.type == TEST_KDP_TYPE
    kdp_clause = Node.objects.filter(type=TEST_KDP_TYPE).first()
    assert kdp_clause is not None
