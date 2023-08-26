from collective.mastodon.interpolators.adapters import tag_from_keyword
from plone import api
from plone.stringinterp.interfaces import IStringInterpolator

import pytest


class TestTagFromKeyword:
    @pytest.mark.parametrize(
        "keyword,tag",
        [
            ("#Plone", "#Plone"),
            ("Plone", "#Plone"),
            ("plone", "#plone"),
            ("Open Source", "#OpenSource"),
            ("open source", "#opensource"),
            ("PloneGov-BR", "#PloneGovBR"),
            ("#PloneGov-BR", "#PloneGovBR"),
            ("IPO$", "#IPO"),
        ],
    )
    def test_tag_from_keyword(self, keyword: str, tag: str):
        assert tag_from_keyword(keyword) == tag


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
