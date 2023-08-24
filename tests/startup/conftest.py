import pytest


APPS = [
    # Missing user attribute
    {
        "name": "localhost-admin",
        "instance": "http://localhost",
        "token": "jutbgrhNDS1EvUvpoHD0ox4a7obSCT9_IpliStv799M",
    },
    # Missing token attribute
    {
        "name": "mastodon.localhost-plone",
        "instance": "http://mastodon.localhost",
        "user": "plone",
    },
    # Good entry
    {
        "name": "mastodon.localhost-foo",
        "instance": "http://mastodon.localhost",
        "token": "jutbgrhNDS1EvUvpoHD0ox4a7obSCT9_IpliStv799M",
        "user": "foo",
    },
]


@pytest.fixture
def mock_settings_mastodon_apps(mocker):
    mocker.patch("collective.mastodon.settings.get_mastodon_apps", return_value=APPS)
