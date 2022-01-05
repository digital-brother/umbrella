"""This file is used for testing 'lease' model"""
import pytest
from umbrella.models.lease import Lease


@pytest.mark.django_db
def test_lease_model():
    """This function is used for testing 'lease' create"""

    test_file_name = "test-file"
    test_pdf = "test-pdf".encode("ascii")
    test_txt = "test-txt"
    test_extracted = "test-extracted"
    test_address = "test-address"

    test_lease = Lease(
        id=1,
        file_name=test_file_name,
        pdf=test_pdf,
        txt=test_txt,
        extracted=test_extracted,
        address=test_address,
    )
    test_lease.save()

    assert test_lease.id == 1
    assert test_lease.file_name == test_file_name
    assert test_lease.txt == test_txt
    assert test_lease.extracted == test_extracted
    assert test_lease.address == test_address
