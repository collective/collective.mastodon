from dataclasses import dataclass
from datetime import datetime
from typing import BinaryIO
from typing import List
from zope.interface import Interface


@dataclass
class MastodonAppInfo:
    """Mastodon App Information."""

    name: str
    instance: str
    user: str
    token: str


@dataclass
class MastodonMedia:
    """Mastodon media object."""

    file: BinaryIO
    mime_type: str
    description: str


class IMastodonRegistry(Interface):
    """A singleton utility listing a."""

    def get_app(name):
        """Returns a MastodonApp."""

    def get_apps():
        """Returns a list of registered apps."""


class IMastodonApp(Interface):
    """A named utility for mastodon."""

    def status_post(
        status: str,
        media_list: List[MastodonMedia],
        sensitive: bool,
        visibility: str,
        spoiler_text: str,
        language: str,
        idempotency_key: str,
        scheduled_at: datetime,
    ):
        """Post a status."""

    def scheduled_statuses():
        """Return a list of scheduled statuses."""
