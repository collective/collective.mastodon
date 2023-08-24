from collective.mastodon import _
from collective.mastodon import utils
from collective.mastodon.app import MastodonApp
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.dexterity.content import DexterityContent
from plone.stringinterp.interfaces import IStringInterpolator
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from threading import Thread
from typing import Any
from zope import schema
from zope.component import adapter
from zope.i18nmessageid import Message
from zope.interface import implementer
from zope.interface import Interface


DEFAULT_STATUS = """${title}, ${description}
${tags}
${url}
"""


def safe_attr(element: "MastodonAction", attr: str) -> Any:
    """Return attribute value."""
    value = getattr(element, attr)
    return value if value is not None else ""


class IMastodonAction(Interface):
    """Definition of the configuration available for a mastodon action."""

    app = schema.Choice(
        title=_("Mastodon App"),
        description=_("App to be used"),
        vocabulary="collective.mastodon.apps",
        required=True,
    )
    visibility = schema.Choice(
        title=_("Visibility"),
        description=_("Visibility of the post"),
        vocabulary="collective.mastodon.visibility",
        default="public",
        required=True,
    )
    spoiler_text = schema.TextLine(
        title=_("Spoiler Text"),
        description=_("Text used for warning."),
        default="",
        required=False,
    )
    language = schema.TextLine(
        title=_("Language"),
        description=_("If not set, the content language will be used."),
        default="",
        required=False,
    )
    sensitive = schema.Bool(
        title=_("Sensitive Content"),
        description=_("Is this a sensitive content?"),
        default=False,
        required=False,
    )
    scheduling = schema.Bool(
        title=_("Schedule post?"),
        description=_("If content effective date is in the future, schedule the post"),
        default=True,
        required=False,
    )
    status = schema.Text(
        title=_("Status"),
        description=_("Main text of the post."),
        default=DEFAULT_STATUS,
        required=True,
    )


@implementer(IMastodonAction, IRuleElementData)
class MastodonAction(SimpleItem):
    """The implementation of the action defined before."""

    app: str = ""
    visibility: str = ""
    spoiler_text: str = ""
    language: str = ""
    sensitive: bool = False
    scheduling: bool = True
    status: str = ""

    element: str = "plone.actions.Mastodon"

    @property
    def _app(self) -> MastodonApp:
        return utils.get_app(self.app)

    @property
    def summary(self) -> Message:
        app = self._app
        username = utils.mastodon_username(app.instance, app.user)
        return _(
            "Post a new toot as ${user}",
            mapping=dict(user=username),
        )


@implementer(IExecutable)
@adapter(Interface, IMastodonAction, Interface)
class MastodonActionExecutor:
    """Executor for the Mastodon Action."""

    content: DexterityContent

    def __init__(self, context, element: "MastodonAction", event):
        """Initialize action executor."""
        self.context = context
        self.element = element
        self.event = event
        self.content = event.object
        self.app = utils.get_app(element.app)

    def _prepare_payload(self) -> dict:
        """Process the action and return a dictionary with the Mastodon message payload.

        :returns: Mastodon message payload.
        """
        content = self.content
        element = self.element
        interpolator = IStringInterpolator(content)
        status = interpolator(safe_attr(element, "status")).strip()
        spoiler_text = interpolator(safe_attr(element, "spoiler_text")).strip()
        sensitive = safe_attr(element, "sensitive")
        visibility = safe_attr(element, "visibility")
        idempotency_key = api.content.get_uuid(content)
        language = safe_attr(element, "language")
        if not language:
            language = content.language[:2] if content.language else None
        media_list = []
        media = utils.media_from_content(content)
        if media:
            media_list = [media]
        payload = {
            "status": status,
            "media_list": media_list,
            "sensitive": sensitive,
            "visibility": visibility,
            "spoiler_text": spoiler_text,
            "language": language,
            "idempotency_key": idempotency_key,
        }
        scheduling = safe_attr(element, "scheduling")
        if scheduling:
            payload["scheduled_at"] = utils.schedule_date(content)
        return payload

    def _post(self, payload: dict) -> Thread:
        """Post a status to Mastodon."""
        app = self.app
        return app.status_post(**payload)

    def __call__(self) -> bool:
        """Execute the action."""
        payload = self._prepare_payload()
        self._post(payload)
        return True


class MastodonAddForm(ActionAddForm):
    """An add form for the Mastodon Action."""

    schema = IMastodonAction
    label = _("Add Mastodon Action")
    description = _("Action to post a toot to a Mastodon account.")
    form_name = _("Configure element")
    Type = MastodonAction

    # custom template will allow us to add help text
    template = ViewPageTemplateFile("mastodon.pt")


class MastodonAddFormView(ContentRuleFormWrapper):
    """Wrapped add form for Mastodon Action."""

    form = MastodonAddForm


class MastodonEditForm(ActionEditForm):
    """An edit form for the mastodon action."""

    schema = IMastodonAction
    label = _("Edit Mastodon Action")
    description = _("Action to post a toot to a Mastodon account.")
    form_name = _("Configure element")

    # custom template will allow us to add help text
    template = ViewPageTemplateFile("mastodon.pt")


class MastodonEditFormView(ContentRuleFormWrapper):
    """Wrapped edit form for Mastodon Action."""

    form = MastodonEditForm
