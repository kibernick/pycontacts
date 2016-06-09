from .models import (
    EmailAddress,
    Group,
    PhoneNumber,
    Person,
    StreetAddress,
)


class AddressBook:

    def __init__(self):
        self._store = {}

    def __repr__(self):
        return "<{}{}>".format(self.__class__.__name__,
                               self._store)

    def EmailAddress(self, *args, **kwargs):
        return EmailAddress(book=self, *args, **kwargs)

    def Group(self, *args, **kwargs):
        return Group(book=self, *args, **kwargs)

    def PhoneNumber(self, *args, **kwargs):
        return PhoneNumber(book=self, *args, **kwargs)

    def Person(self, *args, **kwargs):
        return Person(book=self, *args, **kwargs)

    def StreetAddress(self, *args, **kwargs):
        return StreetAddress(book=self, *args, **kwargs)
