from base64 import b64decode
from collections import defaultdict
from collective.mastodon.testing import INTEGRATION_TESTING
from DateTime import DateTime
from plone import api
from plone.app.multilingual.interfaces import ITranslationManager
from plone.namedfile import NamedBlobImage
from pytest_plone import fixtures_factory
from typing import List
from zope.component.hooks import setSite

import pytest


pytest_plugins = ["pytest_plone"]

globals().update(fixtures_factory(((INTEGRATION_TESTING, "integration"),)))

APPS = [
    {
        "name": "localhost-admin",
        "instance": "http://localhost",
        "token": "jutbgrhNDS1EvUvpoHD0ox4a7obSCT9_IpliStv799M",
        "user": "admin",
    },
    {
        "name": "mastodon.localhost-plone",
        "instance": "http://mastodon.localhost",
        "token": "jutbgrhNDS1EvUvpoHD0ox4a7obSCT9_IpliStv799M",
        "user": "plone",
    },
]


@pytest.fixture
def mock_settings_mastodon_apps(mocker):
    mocker.patch("collective.mastodon.settings.get_mastodon_apps", return_value=APPS)


@pytest.fixture(scope="module")
def vcr_config():
    return dict(
        match_on=["method", "path", "query", "body"], decode_compressed_response=True
    )


@pytest.fixture
def contents() -> List:
    """Content to be created."""
    future_effective_date = DateTime() + 2  # Two days in the future
    past_effective_date = DateTime() - 2  # Two days in the past
    return [
        {
            "_container": "",
            "type": "Image",
            "id": "an-image",
            "title": "A Random Image",
            "description": "With some details",
            "language": "de",
            "subject": ["Image", "Plone"],
            "_image": b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjCDO+/R8ABKsCZD++CcMAAAAASUVORK5CYII=",  # noQA
        },
        {
            "_container": "",
            "type": "Document",
            "id": "future",
            "title": "Future",
            "description": "A document in the future",
            "effective_date": future_effective_date,
            "subject": ["Future", "Mastodon"],
        },
        {
            "_container": "",
            "type": "Document",
            "id": "past",
            "title": "Past",
            "description": "A document in the past",
            "effective_date": past_effective_date,
            "subject": ["Past", "Mastodon"],
        },
        {
            "_container": "",
            "type": "Document",
            "id": "document_preview",
            "title": "Illustrated document",
            "description": "A document with a preview image",
            "effective_date": past_effective_date,
            "subject": ["Preview", "Mastodon"],
            "preview_caption_link": "An image",
            "_preview_image_link": "/an-image",
        },
        {
            "_container": "",
            "type": "News Item",
            "id": "mynews",
            "title": "A News Item",
            "description": "A News Item about Mastodon",
            "subject": ["News", "Mastodon"],
            "_image": b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjCDO+/R8ABKsCZD++CcMAAAAASUVORK5CYII=",  # noQA
        },
    ]


@pytest.fixture
def create_contents(contents):
    """Helper fixture to create initial content."""

    def func(portal) -> dict:
        ids = defaultdict(list)
        for item in contents:
            container_path = item["_container"]
            container = portal.unrestrictedTraverse(container_path)
            payload = {"container": container, "language": "en"}
            if "_image" in item:
                payload["image"] = NamedBlobImage(b64decode(item["_image"]))
            for key, value in item.items():
                if key.startswith("_"):
                    continue
                payload[key] = value
            content = api.content.create(**payload)
            content.language = payload["language"]
            # Relation via preview_image_link
            if "_preview_image_link" in item:
                target = api.content.get(item["_preview_image_link"])
                api.relation.create(content, target, "preview_image_link")
            # Set translation
            if "_translation_of" in item:
                source = portal.unrestrictedTraverse(item["_translation_of"])
                ITranslationManager(source).register_translation(
                    content.language, content
                )
            # Transition items
            if "_transitions" in item:
                transitions = item["_transitions"]
                for transition in transitions:
                    api.content.transition(content, transition=transition)
            content.reindexObject()
            ids[container_path].append(content.getId())
        return ids

    return func


@pytest.fixture()
def update_behaviors(get_fti):
    def update_behaviors(
        type_name: str, add: List[str] = None, remove: List[str] = None
    ):
        """Add a behavior to a content type."""
        from plone.dexterity.schema import invalidate_cache

        fti = get_fti(type_name)
        current = list(fti.behaviors)
        behaviors = [beh for beh in current if beh not in remove] + add
        fti.behaviors = tuple(behaviors)
        invalidate_cache(fti)
        return fti.behaviors

    return update_behaviors


@pytest.fixture
def app(integration, mock_settings_mastodon_apps):
    from collective.mastodon import logger
    from collective.mastodon.startup import register_apps

    register_apps(logger)
    return integration["app"]


@pytest.fixture()
def portal(app, create_contents, update_behaviors):
    """Plone portal with additional content."""
    portal = app["plone"]
    setSite(portal)
    with api.env.adopt_roles(["Manager"]):
        update_behaviors(
            type_name="Document",
            remove=["volto.preview_image"],
            add=["volto.preview_image_link"],
        )
        content_ids = create_contents(portal)

    yield portal
    with api.env.adopt_roles(["Manager"]):
        containers = sorted([path for path in content_ids.keys()], reverse=True)
        for container_path in containers:
            container = portal.unrestrictedTraverse(container_path)
            container.manage_delObjects(content_ids[container_path])


@pytest.fixture
def post_payload():
    def post_payload(**kwargs):
        payload = {
            "status": "Just a toot, with #tags",
            "media_list": [],
            "sensitive": False,
            "visibility": "public",
            "spoiler_text": "",
            "language": "en",
        }
        # Override default values
        if kwargs:
            payload.update(kwargs)
        return payload

    return post_payload


@pytest.fixture
def wait_for():
    def func(thread):
        if not thread:
            return
        thread.join()

    return func
