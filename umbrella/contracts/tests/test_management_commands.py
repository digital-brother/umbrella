from uuid import UUID

import pytest
from django.core.management import call_command

from config.settings.common import ROOT_DIR
from umbrella.contracts.tests.factories import ContractFactory

pytestmark = pytest.mark.django_db

TEST_CONTRACT_FILES_DIR = \
    ROOT_DIR / "umbrella/contracts/test_analytics_jsons/6cb7fa02-457f-4e91-be84-3bfea7692d6b"
TEST_CONTRACT_UUID = str(TEST_CONTRACT_FILES_DIR).split('/')[-1]
TEST_KDP_TYPE = "start"
TEST_CLAUSE_TYPE = "term"
TEST_CLAUSE_PARAGRAPH_ID = 24


def test_parse_contract_command(client):
    contract = ContractFactory(id=UUID(TEST_CONTRACT_UUID))
    call_command('parse_contract', TEST_CONTRACT_FILES_DIR)

    contract_terms = contract.clauses.filter(type=TEST_CLAUSE_TYPE)
    term = contract_terms.filter(content__paraId=TEST_CLAUSE_PARAGRAPH_ID).first()
    assert term

    term_kdps = term.kdps.filter(type=TEST_KDP_TYPE)
    kdp = term_kdps.filter(content__paraId=TEST_CLAUSE_PARAGRAPH_ID).first()
    assert kdp
