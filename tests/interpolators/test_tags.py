from plone import api
from plone.stringinterp.interfaces import IStringInterpolator

import pytest


class TestInterpolatorsTags:
    @pytest.fixture(autouse=True)
    def _init(self, portal):
        self.portal = portal

    @pytest.mark.parametrize(
        "path,expected",
        [
            ("/an-image", "#Image #Plone"),
            ("/document_preview", "#Preview #Mastodon"),
            ("/future", "#Future #Mastodon"),
            ("/past", "#Past #Mastodon"),
            ("/mynews", "#News #Mastodon"),
        ],
    )
    def test_tags(self, path: str, expected: str):
        content = api.content.get(path=path)
        interpolator = IStringInterpolator(content)
        result = interpolator("${tags}")
        assert result == expected
