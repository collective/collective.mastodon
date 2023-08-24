from collective.mastodon.interfaces import IMastodonRegistry
from collective.mastodon.registry import MastodonRegistry
from zope.component import getUtility

import pytest


class TestRegistry:
    @pytest.fixture(autouse=True)
    def _init(self, app):
        self.zope_app = app

    def test_registry_discovery(self):
        registry = getUtility(IMastodonRegistry)
        assert isinstance(registry, MastodonRegistry)

    def test_registry_get_apps(self):
        registry = getUtility(IMastodonRegistry)
        apps = registry.get_apps()
        assert len(apps) == 2

    def test_registry_get_app(self):
        registry = getUtility(IMastodonRegistry)
        name = "localhost-admin"
        app = registry.get_app(name=name)
        assert app.name == name
