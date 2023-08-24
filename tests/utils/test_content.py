from collective.mastodon.interfaces import MastodonMedia
from collective.mastodon.utils import content
from datetime import datetime
from datetime import timedelta
from DateTime import DateTime
from plone import api

import pytest


class TestUtilsContentScheduleAt:
    @property
    def func(self):
        return content._schedule_at

    def test_schedule_at_zope_datetime_future(self):
        value = DateTime() + 1
        result = self.func(value)
        assert isinstance(result, datetime)

    def test_schedule_at_zope_datetime_past(self):
        value = DateTime() - 1
        result = self.func(value)
        assert result is None

    def test_schedule_at_stdlib_datetime_future(self):
        value = datetime.now() + timedelta(days=1)
        result = self.func(value)
        assert isinstance(result, datetime)

    def test_schedule_at_stdlib_datetime_past(self):
        value = datetime.now() - timedelta(days=1)
        result = self.func(value)
        assert result is None


class TestUtilsContentScheduleDate:
    @property
    def func(self):
        return content.schedule_date

    @pytest.fixture(autouse=True)
    def _init(self, portal):
        self.portal = portal

    @pytest.mark.parametrize(
        "path,expected",
        [
            ("/an-image", False),
            ("/document_preview", False),
            ("/future", True),
            ("/past", False),
            ("/mynews", False),
        ],
    )
    def test_schedule_date(self, path: str, expected: bool):
        content = api.content.get(path=path)
        result = self.func(content)
        if expected:
            assert isinstance(result, datetime)
        else:
            assert result is None


class TestUtilsContentMediaFromContent:
    @property
    def func(self):
        return content.media_from_content

    @pytest.fixture(autouse=True)
    def _init(self, portal):
        self.portal = portal

    @pytest.mark.parametrize(
        "path,expected",
        [
            ("/an-image", True),
            ("/document_preview", True),
            ("/future", False),
            ("/past", False),
            ("/mynews", True),
        ],
    )
    def test_media_from_content(self, path: str, expected: bool):
        content = api.content.get(path=path)
        result = self.func(content)
        if not expected:
            assert result is None
        else:
            assert isinstance(result, MastodonMedia)

    @pytest.mark.parametrize(
        "path,expected",
        [
            # Description
            ("/an-image", "With some details"),
            # preview_caption_link
            ("/document_preview", "An image"),
            # No image_caption, fallback to title
            ("/mynews", "A News Item"),
        ],
    )
    def test_media_from_content_description(self, path: str, expected: str):
        content = api.content.get(path=path)
        result = self.func(content)
        assert result.description == expected
