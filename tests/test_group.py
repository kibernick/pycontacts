def test_get_members(address_book, sample_persons):
    john, _ = sample_persons
    group = address_book.groups.create(name="Sampled")
    group.save()
    john['groups'] = [group]
    john.save()

    persons = group.get_members()
    assert len(persons) == 1
    assert persons[0].id == john.id
