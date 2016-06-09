[![Build Status](https://drone.io/github.com/kibernick/pycontacts/status.png)](https://drone.io/github.com/kibernick/pycontacts/latest)

# pycontacts

A delightfully simple address book library in Python.

The purpose of this repo is to demonstrate how to create a simple Python library that provides an API for others to interact with. Internally it's using pure Python and nothing else.

# Installation

Install the library within your (virtual) environment with:

`python setup.py install`

The only dependencies are related to running tests and are found in the `dev-requirements.txt` file.

# Usage

An AddressBook's entities include Persons, Groups, EmailAddresses and others. The common API to interact with these entities goes as follows:

```python
from pycontacts import AddressBook
book = AddressBook()

email = book.email_addresses.create(email="example@email.com")
email.save()
```

## Add a Person to the address book.

```python
person = book.persons.create(first_name="Jack", last_name="Harkness")

street_address = book.street_addresses.create(address_line="Torch Woods 12").save()
person['street_addresses'].append(street_address)

email_address = book.email_addresses.create(email="jack@example.com").save()
person['email_addresses'].append(email_address)

phone_number = book.phone_numbers.create(phone="+14155552671").save()
person['phone_numbers'].append(phone_number)

person.save()
```

## Add a Group to the address book

```python
group = book.groups.create(name="The Examples").save()
```

## Given a group we want to easily find its members

```python
group.get_members()
```

## Given a person we want to easily find the groups the person belongs to

```python
person.get_groups()
```

## Find person by name (can supply either first name, last name, or both)

```python
book.persons.find_by_name(first_name="Jan")
book.persons.find_by_name(last_name="Tesla")
book.persons.find_by_name(first_name="Adam", last_name="Young")
```

## Find person by email address (can supply either the exact string or a prefix string, ie. both "alexander@company.com" and "alex" should work)

Currently implemented as exact match only.

```python
book.persons.find_by_email(email="newton@example.com")
```

# Design discussion

## Find person by email address for any substring

The simplest solution in the currect setup would be to change the `BaseManager.filter` method to optionally accomodate for inexact matches, with a suffix added to the kwarg.

For example, by being able to call: `persons.filter(email__contains="thomas"` we would then get all email addresses containing this substring. We should be to implement this and other similar "field lookups" by abstracting the `filter` method.
