from pycontacts import AddressBook
from pycontacts.models import Person


def test_create_book():
    book = AddressBook()
    assert book._store is not None
    assert isinstance(book._store, dict)


def test_create_person_model_class():
    book = AddressBook()
    p = book.Person()
    assert isinstance(p, Person)
    assert p._book is not None
    assert isinstance(p._book, AddressBook)
    assert p._book._store is book._store
