from collective.mastodon.utils import tools

import pytest


class TestUtilsTools:
    @pytest.mark.parametrize(
        "name,instance,user",
        [
            ("localhost-admin", "http://localhost", "admin"),
            ("mastodon.localhost-plone", "http://mastodon.localhost", "plone"),
        ],
    )
    def test_mastodon_username(self, app, name: str, instance: str, user: str):
        func = tools.get_app
        app = func(name)
        assert app.instance == instance
        assert app.user == user
