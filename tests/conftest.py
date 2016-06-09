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


@pytest.fixture
def sample_persons(address_book):
    person1_email = address_book.email_addresses.create(email="johnlocke@lost.com")
    person1_email.save()
    person1 = address_book.persons.create(
        first_name="John", last_name="Locke", email_addresses=[person1_email])
    person1.save()

    person2 = address_book.persons.create(first_name="Kate", last_name="Austen")
    person2.save()
    return person1, person2
