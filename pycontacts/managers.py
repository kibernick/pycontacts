from .models import (
    EmailAddress,
    Group,
    PhoneNumber,
    Person,
    StreetAddress,
)
from .exceptions import ImproperlyConfigured


class BaseManager:
    cls = None  # Override this in a concrete manager

    def __init__(self, book):
        self._book = book

    def _get_table(self):
        return self._book._store[self.cls.table_name]

    def filter(self, table=None, **kwargs):
        """
        Filter per multiple kwargs, is not exclusive with matches.
        :param table: table as dict.
        :param attr: attribute name to compare.
        :param val: attribute value to compare.
        :return: result dict by object ids.
        """
        if table is None:
            table = self._get_table()
        results = {}
        for obj_id, obj_attrs in table.items():
            for attr, val in kwargs.items():
                if obj_attrs[attr] == val:
                    results[obj_id] = obj_attrs
        return results

    def convert_results(self, results):
        cls_objects = []
        for r_id, r_attrs in results.items():
            cls_obj = self.create(**r_attrs)
            cls_obj._uuid = r_id
            cls_objects.append(cls_obj)
        return cls_objects

    def create(self, **kwargs):
        if not self.cls:
            raise ImproperlyConfigured("'cls' not overriden")
        return self.cls(book=self._book, **kwargs)


class EmailAddressManager(BaseManager):
    cls = EmailAddress


class PhoneNumberManager(BaseManager):
    cls = PhoneNumber


class StreetAddressManager(BaseManager):
    cls = StreetAddress


class GroupManager(BaseManager):
    cls = Group


class PersonManager(BaseManager):
    cls = Person

    def find_by_name(self, first_name=None, last_name=None):
        """
        Get all matches for first_name and last_name.
        """
        if not (first_name or last_name):
            raise ValueError("Supply either 'first_name', 'last_name', or both")

        table = self._get_table()
        results = self.filter(table, first_name=first_name, last_name=last_name)
        return self.convert_results(results)
