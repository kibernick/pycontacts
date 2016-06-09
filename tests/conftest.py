import pytest

from pycontacts import AddressBook
from pycontacts.models import BaseModel


class ExtenedBaseModel(BaseModel):
    table_name = 'tests'
    attributes = (
        'test_set',
        'test_not_set',
    )


@pytest.fixture
def address_book():
    return AddressBook()


@pytest.fixture
def extended_instance(address_book):
    return ExtenedBaseModel(book=address_book, test_set=123)
