import pytest


def test_find_by_first_name(address_book, sample_persons):
    persons = address_book.persons.find_by_name(first_name="John")
    assert len(persons) == 1
    assert persons[0]['first_name'] == 'John'


def test_find_by_last_name(address_book, sample_persons):
    persons = address_book.persons.find_by_name(last_name="Austen")
    assert len(persons) == 1
    assert persons[0]['last_name'] == 'Austen'


def test_find_by_first_and_last_name(address_book, sample_persons):
    persons = address_book.persons.find_by_name(first_name="John",
                                                last_name="Austen")
    assert len(persons) == 2


def test_find_by_name_error(address_book):
    with pytest.raises(ValueError):
        address_book.persons.find_by_name()


def test_find_by_email(address_book, sample_persons):
    persons = address_book.persons.find_by_email(email="johnlocke@lost.com")

    assert len(persons) == 1
