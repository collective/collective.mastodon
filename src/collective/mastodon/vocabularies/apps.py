from collective.mastodon.interfaces import IMastodonRegistry
from collective.mastodon.utils import mastodon_username
from zope.component import getUtility
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def mastodon_apps(_):
    """List registered Mastodon apps."""
    registry = getUtility(IMastodonRegistry)
    apps = registry.get_apps()
    terms = []
    for app in apps:
        title = mastodon_username(app.instance, app.user)
        terms.append(SimpleTerm(value=app.name, token=app.name, title=title))

    return SimpleVocabulary(terms)
