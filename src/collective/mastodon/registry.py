from collective.mastodon.app import MastodonApp
from collective.mastodon.interfaces import IMastodonApp
from collective.mastodon.interfaces import IMastodonRegistry
from typing import List
from zope.component import getAllUtilitiesRegisteredFor
from zope.component import getUtility
from zope.interface import implementer


@implementer(IMastodonRegistry)
class MastodonRegistry:
    """Mastodon Utility"""

    def get_app(self, name: str) -> MastodonApp:
        """Return a named Mastodon application."""
        return getUtility(IMastodonApp, name=name)

    def get_apps(self) -> List[MastodonApp]:
        """Return a list of registered Mastodon applications."""
        return getAllUtilitiesRegisteredFor(IMastodonApp)
