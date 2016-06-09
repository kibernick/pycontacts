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
