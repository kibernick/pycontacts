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
        self.book = book

    def _get_table(self):
        return self.book._store[self.cls.table_name]

    def filter(self, **kwargs):
        """
        Filter per multiple kwargs, is not exclusive with matches.
        'table' is a reserved kwarg.
        :param table: table as dict.
        :param attr: attribute name to compare.
        :param val: attribute value to compare.
        :return: result dict by object ids.
        """
        table = kwargs.pop('table', None)
        if not table:
            table = self._get_table()
        results = {}
        for obj_id, obj_attrs in table.items():
            for attr, qry_val in kwargs.items():
                obj_val = obj_attrs[attr]
                # If 'qval' is a list check for membership.
                if isinstance(qry_val, list):
                    # We could be checking in a foreign keys column (list).
                    if isinstance(obj_val, list):
                        if set(obj_val).intersection(set(qry_val)):
                            results[obj_id] = obj_attrs
                    # Otherwise check if the object's value is in query list.
                    elif obj_val in qry_val:
                            results[obj_id] = obj_attrs
                # We are checking for a single query value.
                else:
                    if isinstance(obj_val, list):
                        if qry_val in obj_val:
                            results[obj_id] = obj_attrs
                    elif obj_attrs[attr] == qry_val:
                        results[obj_id] = obj_attrs
        return results

    def convert_results(self, results):
        cls_objects = []
        for r_id, r_attrs in results.items():
            cls_obj = self.create(**r_attrs)
            cls_obj.id = r_id
            cls_objects.append(cls_obj)
        return cls_objects

    def create(self, **kwargs):
        if not self.cls:
            raise ImproperlyConfigured("'cls' not overriden")
        return self.cls(book=self.book, **kwargs)


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

        results = self.filter(first_name=first_name, last_name=last_name)
        return self.convert_results(results)

    def find_by_email(self, email):
        """
        Search for Persons by their EmailAddress (given as "email" string).
        """
        emails = EmailAddressManager(self.book)
        email_results = emails.filter(email=email)
        email_ids = email_results.keys()

        person_results = self.filter(email_addresses_ids=email_ids)
        return self.convert_results(person_results)
