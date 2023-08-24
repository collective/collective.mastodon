from collective.mastodon.app import MastodonApp
from collective.mastodon.interfaces import IMastodonRegistry
from zope.component import getUtility


def get_app(name: str) -> MastodonApp:
    """Given a name, return a MastodonApp."""
    util = getUtility(IMastodonRegistry)
    return util.get_app(name)
