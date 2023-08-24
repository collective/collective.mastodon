from collective.mastodon.app import MastodonApp
from collective.mastodon.interfaces import IMastodonApp
from collective.mastodon.utils import media_from_content
from datetime import datetime
from plone import api
from zope.component import getAllUtilitiesRegisteredFor
from zope.component import getUtility

import pytest
import pytz


DEFAULT_APP = "localhost-admin"


class TestAppDiscovery:
    @pytest.fixture(autouse=True)
    def _init(self, app):
        self.zope_app = app

    def test_all_apps(self):
        all_apps = getAllUtilitiesRegisteredFor(IMastodonApp)
        assert len(all_apps) == 2

    @pytest.mark.parametrize(
        "name,instance,user",
        [
            ("localhost-admin", "http://localhost", "admin"),
            ("mastodon.localhost-plone", "http://mastodon.localhost", "plone"),
        ],
    )
    def test_app_is_registered(self, name: str, instance: str, user: str):
        app = getUtility(IMastodonApp, name=name)
        assert isinstance(app, MastodonApp)
        assert app.name == name
        assert app.instance == instance
        assert app.user == user


class TestAppMethods:
    app: MastodonApp

    @pytest.fixture(autouse=True)
    def _init(self, portal):
        self.portal = portal
        self.app = getUtility(IMastodonApp, name=DEFAULT_APP)


class TestAppStatusPost(TestAppMethods):
    @pytest.mark.vcr()
    def test_post(self, post_payload):
        payload = post_payload()
        response = self.app._status_post(**payload)
        assert isinstance(response, dict)
        assert "id" in response
        assert response["language"] == "en"
        assert response["visibility"] == "public"
        assert response["sensitive"] is False
        assert "Just a toot" in response["content"]

    @pytest.mark.vcr()
    def test_post_private(self, post_payload):
        payload = post_payload(visibility="private")
        response = self.app._status_post(**payload)
        assert response["visibility"] == "private"

    @pytest.mark.vcr()
    def test_post_sensitive(self, post_payload):
        payload = post_payload(sensitive=True)
        response = self.app._status_post(**payload)
        assert response["sensitive"] is True

    @pytest.mark.vcr()
    def test_post_language(self, post_payload):
        payload = post_payload(language="pt")
        response = self.app._status_post(**payload)
        assert response["language"] == "pt"

    @pytest.mark.vcr()
    def test_post_spoiler_text(self, post_payload):
        payload = post_payload(spoiler_text="Sketch a Day")
        response = self.app._status_post(**payload)
        assert response["spoiler_text"] == "Sketch a Day"

    @pytest.mark.vcr()
    def test_post_scheduled_at(self, post_payload):
        future = datetime(4000, 1, 1, 12, 13, 14, 0, pytz.timezone("Etc/GMT+2"))
        payload = post_payload(scheduled_at=future)
        response = self.app._status_post(**payload)
        scheduled_at = response["scheduled_at"]
        assert scheduled_at.year == future.year
        assert scheduled_at.month == future.month
        assert scheduled_at.day == future.day
        assert response["params"]["text"] == payload["status"]

    @pytest.mark.vcr(match_on=["path"])
    def test_post_media(self, post_payload):
        content = api.content.get("/an-image")
        media_list = [media_from_content(content)]
        payload = post_payload(media_list=media_list)
        response = self.app._status_post(**payload)
        media_attachments = response["media_attachments"]
        assert isinstance(media_attachments, list)
        assert len(media_attachments) == 1
        assert media_attachments[0]["type"] == "image"
        assert media_attachments[0]["meta"]["original"]["width"] == 1
        assert media_attachments[0]["meta"]["original"]["height"] == 1


class TestAppScheduledStatuses(TestAppMethods):
    @pytest.mark.vcr()
    def test_scheduled_posts(self):
        response = self.app.scheduled_statuses()
        assert isinstance(response, list)
        scheduled_post = response[0]
        assert "id" in scheduled_post
        assert "scheduled_at" in scheduled_post
