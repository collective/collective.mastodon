from collective.mastodon import _
from plone.base import PloneMessageFactory as _PM
from plone.stringinterp.adapters import BaseSubstitution
from Products.CMFCore.interfaces import IDublinCore
from zope.component import adapter


TRANSLATION_TABLE = str.maketrans(
    {
        "-": "",
        "_": "",
        "#": "",
        "$": "",
        ".": "",
        " ": "",
    }
)


def tag_from_keyword(keyword: str) -> str:
    """Convert a keyword to a tag."""
    keyword = keyword.translate(TRANSLATION_TABLE)
    return f"#{keyword}"


@adapter(IDublinCore)
class TagsSubstitution(BaseSubstitution):
    category = _PM("Dublin Core")
    description = _("Tags")

    def safe_call(self):
        tags = [tag_from_keyword(item) for item in self.context.Subject()]
        return " ".join(tags)
