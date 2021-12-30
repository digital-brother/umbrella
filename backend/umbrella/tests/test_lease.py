from datetime import datetime

import pytest
from umbrella.models.Lease import Lease


@pytest.mark.django_db
def testLeaseModel():
    assert Lease.objects.count() == 0

    TEST_FILE_NAME = "test-file"
    TEST_PDF = "test-pdf".encode("ascii")
    TEST_TXT = "test-txt"
    TEST_EXTRACTED = "test-extracted"
    TEST_ADDRESS = "test-address"

    testLease = Lease.objects.create(
        id=1,
        file_name=TEST_FILE_NAME,
        pdf=TEST_PDF,
        txt=TEST_TXT,
        extracted=TEST_EXTRACTED,
        address=TEST_ADDRESS,
    )
    assert Lease.objects.count() == 1
    assert testLease.id == 1
    assert testLease.file_name == TEST_FILE_NAME
    assert testLease.txt == TEST_TXT
    assert testLease.extracted == TEST_EXTRACTED
    assert testLease.address == TEST_ADDRESS
