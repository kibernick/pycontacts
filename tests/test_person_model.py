def test_get_groups(sample_persons, sample_group):
    john, _ = sample_persons
    john['groups'] = [sample_group]
    john.save()

    groups = john.get_groups()
    assert len(groups) == 1
    assert groups[0].id == sample_group.id
