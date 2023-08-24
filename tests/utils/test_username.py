from collective.mastodon.utils import username

import pytest


class TestUtilsUsername:
    @pytest.mark.parametrize(
        "instance,user,expected",
        [
            ("http://localhost", "user", "@user@localhost"),
            ("http://mastodon.localhost", "user", "@user@mastodon.localhost"),
            ("https://pynews.com.br", "ericof", "@ericof@pynews.com.br"),
            ("https://fosstodon.org", "ericof", "@ericof@fosstodon.org"),
        ],
    )
    def test_mastodon_username(self, instance: str, user: str, expected: str):
        func = username.mastodon_username
        assert func(instance, user) == expected
