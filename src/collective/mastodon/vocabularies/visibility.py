from collective.mastodon import _
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


TERMS = [
    ("public", _("Public")),
    ("unlisted", _("Unlisted")),
    ("private", _("Private")),
    ("direct", _("Direct")),
]


@provider(IVocabularyFactory)
def post_visibility(context):
    """Mastodon post visibility."""
    terms = []
    for token, title in TERMS:
        terms.append(SimpleTerm(value=token, token=token, title=title))

    return SimpleVocabulary(terms)
