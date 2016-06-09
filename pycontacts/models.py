import importlib
import uuid

from .exceptions import ImproperlyConfigured, InstanceDoesNotExist


class BaseModel(dict):
    """
    Provide an elementary way of saving instance data.
    """
    table_name = None  # "table" to save this model to
    attributes = None  # Set this as tuple of strings.
    foreign_keys = {}  # str -> class

    def __init__(self, book, **kwargs):
        """
        Need to provide an AddressBook instance as a first argument.
        Model attributes can be initialised with kwargs.
        Foreign keys are received as lists of objects of appropriate type.

        Example foreign keys in kwarg:
        "phone_numbers": [<PhoneNumber>, <...>]

        """
        self.id = None  # unique identifier of this model instance
        self.book = book
        # Try to fill in values from given kwargs
        if self.attributes:
            self._set_attribute_values(self, source=kwargs)
        for name, cls in self.foreign_keys.items():
            # TODO: validation for type match with cls
            self[name] = kwargs.get(name, [])

    def __repr__(self):
        return "<{}{}>".format(self.__class__.__name__,
                               super(BaseModel, self).__repr__())

    def _check_config(self):
        if self.table_name is None:
            raise ImproperlyConfigured("table_name")
        if self.attributes is None:
            raise ImproperlyConfigured("attributes")
        if self.book is None:
            raise ImproperlyConfigured("book")

    @staticmethod
    def _generate_uuid():
        return uuid.uuid4().hex

    def _set_attribute_values(self, dest, source=None):
        if source is None:
            source = self
        elif not isinstance(source, dict):
            raise ValueError("'source' must be of type 'dict'")
        for attribute_name in self.attributes:
            dest[attribute_name] = source.get(attribute_name)

    def _update_related_object_ids(self, record):
        for list_name, key_class in self.foreign_keys.items():
            column_name = list_name + "_ids"
            related_obj_ids = [o.id for o in self[list_name]]
            record[column_name] = related_obj_ids

    def _get_table(self):
        if self.table_name not in self.book._store:
            self.book._store[self.table_name] = {}
        return self.book._store[self.table_name]

    def _get_record(self, table):
        if not self.id:
            self.id = self._generate_uuid()
        if self.id not in table:
            table[self.id] = {}
        return table[self.id]

    def save(self):
        """
        Technically, does an update of an existing record in store.
        Does not update individual related objects, but keeps a record
        of their IDs.
        """
        self._check_config()
        table = self._get_table()
        record = self._get_record(table)
        self._set_attribute_values(record)
        self._update_related_object_ids(record)
        return self

    def delete(self):
        """
        Remove this record from store, potentially leaves foreign key records as orphaned.
        """
        self._check_config()
        if not self.id:
            raise InstanceDoesNotExist()
        table = self._get_table()
        if self.id not in table:
            raise InstanceDoesNotExist()
        del table[self.id]
        self.id = None
        return self


class EmailAddress(BaseModel):
    table_name = "email_addresses"
    attributes = (
        'email',
    )
    foreign_keys = {}


class StreetAddress(BaseModel):
    table_name = "street_addresses"
    attributes = (
        'address_line',
    )
    foreign_keys = {}


class PhoneNumber(BaseModel):
    table_name = "phone_numbers"
    attributes = (
        'phone',
    )
    foreign_keys = {}


class Group(BaseModel):
    table_name = "groups"
    attributes = (
        'name',
    )
    foreign_keys = {}

    def get_members(self):
        person_results = self.book.persons.filter(groups_ids=self.id)
        return self.book.persons.convert_results(person_results)


class Person(BaseModel):
    table_name = "persons"
    attributes = (
        'first_name',
        'last_name',
    )
    foreign_keys = {
        'email_addresses': EmailAddress,
        'street_addresses': StreetAddress,
        'phone_numbers': PhoneNumber,
        'groups': Group,
    }

    def get_groups(self):
        group_ids = [g.id for g in self['groups']]
        group_results = self.book.groups.filter(id=group_ids)
        return self.book.groups.convert_results(group_results)
