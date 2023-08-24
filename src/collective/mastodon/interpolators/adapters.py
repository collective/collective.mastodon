from collective.mastodon import _
from plone.base import PloneMessageFactory as _PM
from plone.stringinterp.adapters import BaseSubstitution
from Products.CMFCore.interfaces import IDublinCore
from zope.component import adapter


@adapter(IDublinCore)
class TagsSubstitution(BaseSubstitution):
    category = _PM("Dublin Core")
    description = _("Tags")

    def safe_call(self):
        tags = [f"#{item}" for item in self.context.Subject()]
        return " ".join(tags)
