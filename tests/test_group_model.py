def test_get_members(sample_persons, sample_group):
    john, _ = sample_persons
    john['groups'] = [sample_group]
    john.save()

    persons = sample_group.get_members()
    assert len(persons) == 1
    assert persons[0].id == john.id
