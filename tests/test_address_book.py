from pycontacts import AddressBook
from pycontacts.models import Person
from pycontacts.managers import (
    EmailAddressManager,
    GroupManager,
    PhoneNumberManager,
    PersonManager,
    StreetAddressManager,
)


def test_create_book():
    book = AddressBook()
    assert book._store is not None
    assert isinstance(book._store, dict)


def test_create_person_model_class():
    book = AddressBook()
    p = book.persons.create()
    assert isinstance(p, Person)
    assert p.book is not None
    assert isinstance(p.book, AddressBook)
    assert p.book._store is book._store


def test_create_book_with_managers(address_book):
    assert isinstance(address_book.email_addresses, EmailAddressManager)
    assert isinstance(address_book.groups, GroupManager)
    assert isinstance(address_book.phone_numbers, PhoneNumberManager)
    assert isinstance(address_book.persons, PersonManager)
    assert isinstance(address_book.street_addresses, StreetAddressManager)
