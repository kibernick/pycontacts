import copy
import pytest

from pycontacts.models import BaseModel
from pycontacts.exceptions import ImproperlyConfigured, InstanceDoesNotExist


def test_initialization_base(address_book):
    bm = BaseModel(address_book)
    assert bm.book is address_book
    assert not bm.items()


def test_initialization_extending(address_book, extended_instance):
    assert extended_instance.book is address_book
    assert extended_instance['test_set'] == 123
    assert not extended_instance['test_not_set']


def test_config_check(address_book, extended_instance):
    with pytest.raises(ImproperlyConfigured):
        BaseModel(None)._check_config()
    with pytest.raises(ImproperlyConfigured):
        BaseModel(address_book)._check_config()
    extended_instance._check_config()


def test_generate_uuid(address_book):
    uuid_str = BaseModel(address_book)._generate_uuid()
    assert isinstance(uuid_str, str)


def test_set_attribute_values_self_as_source(extended_instance):
    dest = {}
    extended_instance._set_attribute_values(dest)
    assert dest.items() == extended_instance.items()


def test_set_attribute_values_source_valid(extended_instance):
    dest, source = {}, {"test_set": "Atreides"}
    extended_instance._set_attribute_values(dest, source=source)
    assert dest.keys() == extended_instance.keys()
    assert [x for x in source.values() if x in dest.values()]


def test_set_attribute_values_source_invalid(extended_instance):
    dest, source = {}, ('Harkonnen',)
    with pytest.raises(ValueError):
        extended_instance._set_attribute_values(dest, source=source)


def test_get_table_new(address_book, extended_instance):
    assert extended_instance.table_name not in address_book._store
    table = extended_instance._get_table()
    assert table == {}
    assert extended_instance.table_name in address_book._store


def test_get_table_existing(address_book, extended_instance):
    test_table = {'123': {'name': 'gom jabbar'}}
    address_book._store = {'tests': test_table}
    table = extended_instance._get_table()
    assert table == test_table


def test_get_record_new(extended_instance):
    table = {}
    record = extended_instance._get_record(table)
    assert record == {}
    assert extended_instance.id in table


def test_save(address_book, extended_instance):
    output = extended_instance.save()
    assert output == extended_instance
    table = address_book._store[extended_instance.table_name]
    assert table[extended_instance.id] == extended_instance


def test_delete_no_uuid(extended_instance):
    with pytest.raises(InstanceDoesNotExist):
        extended_instance.delete()


def test_delete_not_in_table(extended_instance):
    extended_instance.id = "123"
    with pytest.raises(InstanceDoesNotExist):
        extended_instance.delete()


def test_delete_ok(address_book, extended_instance):
    extended_instance.save()
    old_id = extended_instance.id
    extended_instance.delete()
    table = address_book._store[extended_instance.table_name]
    assert old_id not in table
    assert extended_instance.id is None


def test_update_related_object_ids(extended_instance):
    extended_instance.foreign_keys = {
        "more_tests": extended_instance.__class__,
    }
    extended_instance['more_tests'] = [
        copy.deepcopy(extended_instance),
    ]
    record = {}
    extended_instance._update_related_object_ids(record)
    assert record['more_tests_ids'] == [
        x.id for x in extended_instance['more_tests']
    ]
