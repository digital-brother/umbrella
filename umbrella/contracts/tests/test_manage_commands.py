import pytest
from django.core.management import call_command
from uuid import UUID

from umbrella.contracts.models import Node
from umbrella.contracts.tests.factories import ContractFactory

pytestmark = pytest.mark.django_db

TEST_CONTRACT_FILES_DIR = "umbrella/contracts/test_analytics_jsons/6cb7fa02-457f-4e91-be84-3bfea7692d6b"
TEST_CONTRACT_UUID = "6cb7fa02-457f-4e91-be84-3bfea7692d6b"
TEST_KDP_TYPE = "start"
TEST_CLAUSE_TYPE = "term"


def test_parse_contract(client):
    contract = ContractFactory(id=UUID(TEST_CONTRACT_UUID))
    assert Node.objects.count() == 0
    call_command('parse_contract', TEST_CONTRACT_FILES_DIR)
    assert Node.objects.count() > 0
    clause = Node.objects.filter(contract=contract, type=TEST_CLAUSE_TYPE).first()
    assert clause is not None
    kdp = Node.objects.filter(clause=clause, type=TEST_KDP_TYPE)
    assert kdp is not None
