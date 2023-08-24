from collective.mastodon.interfaces import IMastodonApp
from zope.component import getAllUtilitiesRegisteredFor

import pytest


class TestRegisterApps:
    @pytest.fixture(autouse=True)
    def _init(self, app):
        self.zope_app = app

    def test_register_apps_result(self):
        apps = getAllUtilitiesRegisteredFor(IMastodonApp)
        assert len(apps) == 1
        assert apps[0].name == "mastodon.localhost-foo"
        assert apps[0].user == "foo"
