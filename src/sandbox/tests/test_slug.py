from slug import slugify


def test_slugify_lowercase_and_dashes_spaces():
    assert slugify("Release Tracker") == "release-tracker"
