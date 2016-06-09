import uuid

from .exceptions import ImproperlyConfigured, InstanceDoesNotExist


class BaseModel(dict):
    """
    Provide an elementary way of saving data.
    """
    table_name = None  # "table" to save this model to
    attributes = None  # Set this as tuple of strings.
    foreign_keys = {}  # str -> class

    def __init__(self, book, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self._uuid = None  # unique identifier of this model instance
        self._book = book
        # Try to fill in values from given kwargs
        if self.attributes:
            self._set_attribute_values(self, source=kwargs)

    def _check_config(self):
        if self.table_name is None:
            raise ImproperlyConfigured("table_name")
        if self.attributes is None:
            raise ImproperlyConfigured("attributes")
        if self._book is None:
            raise ImproperlyConfigured("_book")

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

    def _get_table(self):
        if self.table_name not in self._book._store:
            self._book._store[self.table_name] = {}
        return self._book._store[self.table_name]

    def _get_record(self, table):
        if not self._uuid:
            self._uuid = self._generate_uuid()
        if self._uuid not in table:
            table[self._uuid] = {}
        return table[self._uuid]

    def save(self):
        """
        Technically, does an update of an existing record in store.
        Does not update individual related objects.
        """
        self._check_config()
        table = self._get_table()
        record = self._get_record(table)
        self._set_attribute_values(record)

    def delete(self):
        """
        Remove this record from store, potentially leaves foreign key records as orphaned.
        """
        self._check_config()
        if not self._uuid:
            raise InstanceDoesNotExist()
        table = self._get_table()
        if self._uuid not in table:
            raise InstanceDoesNotExist()
        del table[self._uuid]


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
