from .managers import (
    EmailAddressManager,
    GroupManager,
    PhoneNumberManager,
    PersonManager,
    StreetAddressManager,
)


class AddressBook:

    def __init__(self):
        self._store = {}
        self.email_addresses = EmailAddressManager(self)
        self.groups = GroupManager(self)
        self.phone_numbers = PhoneNumberManager(self)
        self.persons = PersonManager(self)
        self.street_addresses = StreetAddressManager(self)

    def __repr__(self):
        return "<{}{}>".format(self.__class__.__name__,
                               self._store)
