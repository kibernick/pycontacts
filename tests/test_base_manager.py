from pycontacts.managers import BaseManager

from conftest import ExtenedBaseModel


class ExampleManager(BaseManager):
    cls = ExtenedBaseModel


def test_new_manager(address_book):
    examples = ExampleManager(address_book)
    assert examples._book == address_book


def test_manager_create(address_book):
    examples = ExampleManager(address_book)
    empty_example = examples.create()
    assert isinstance(empty_example, ExtenedBaseModel)
    assert not empty_example['test_set']
    assert not empty_example['test_not_set']
