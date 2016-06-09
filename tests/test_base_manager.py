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


def test_manager_filter(address_book):
    examples = ExampleManager(address_book)
    example = examples.create(test_set="Jack")
    example.save()

    results = examples.filter(test_set="Jack")
    assert results.values()[0]['test_set'] == "Jack"


def test_manager_convert_results(address_book):
    examples = ExampleManager(address_book)
    example = examples.create(test_set="Jack")
    example.save()

    results = examples.filter(test_set="Jack")
    example_objs = examples.convert_results(results)
    assert len(example_objs) == 1
    assert isinstance(example_objs[0], ExtenedBaseModel)
    assert example_objs[0]['test_set'] == "Jack"
