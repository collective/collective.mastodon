from collective.mastodon.actions.mastodon import MastodonAction
from collective.mastodon.actions.mastodon import MastodonAddFormView
from collective.mastodon.actions.mastodon import MastodonEditFormView
from plone.app.contentrules.rule import Rule
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface.interfaces import IObjectEvent

import pytest


@pytest.fixture
def action_payload() -> dict:
    return {
        "app": "localhost-admin",
        "visibility": "public",
        "spoiler_text": "${title}",
        "language": "en",
        "sensitive": False,
        "scheduling": True,
        "status": "Hello word! ${tags} ${absolute_url}",
    }


@pytest.fixture
def mastodon_action(action_payload) -> MastodonAction:
    e = MastodonAction()
    for attr, value in action_payload.items():
        setattr(e, attr, value)
    return e


@implementer(IObjectEvent)
class DummyEvent:
    def __init__(self, object):
        self.object = object


class TestAction:
    name: str = "plone.actions.Mastodon"

    @pytest.fixture(autouse=True)
    def _init(self, portal):
        self.portal = portal
        self.image = portal["an-image"]

    def add_view(self, http_request):
        element = getUtility(IRuleAction, name=self.name)
        storage = getUtility(IRuleStorage)
        storage["foo"] = Rule()
        rule = self.portal.restrictedTraverse("++rule++foo")
        adding = getMultiAdapter((rule, http_request), name="+action")
        addview = getMultiAdapter((adding, http_request), name=element.addview)
        return addview

    def test_registered(self):
        element = getUtility(IRuleAction, name=self.name)
        assert self.name == element.addview
        assert "edit" == element.editview
        assert element.for_ is None

    def test_summary(self, mastodon_action):
        from zope.i18nmessageid.message import Message

        summary = mastodon_action.summary
        assert isinstance(summary, Message)
        assert summary == "Post a new toot as ${user}"
        assert summary.mapping == {"user": "@admin@localhost"}

    def test_add_view(self, http_request, action_payload):
        addview = self.add_view(http_request)
        assert isinstance(addview, MastodonAddFormView) is True
        addview.form_instance.update()
        output = addview.form_instance()
        assert "<h2>Substitutions</h2>" in output
        content = addview.form_instance.create(data=action_payload)
        addview.form_instance.add(content)
        rule = self.portal.restrictedTraverse("++rule++foo")
        e = rule.actions[0]
        assert isinstance(e, MastodonAction)
        assert e.app == "localhost-admin"

    def test_edit_view(self, http_request):
        element = getUtility(IRuleAction, name=self.name)
        e = MastodonAction()
        editview = getMultiAdapter((e, http_request), name=element.editview)
        assert isinstance(editview, MastodonEditFormView)

    @pytest.mark.parametrize(
        "key,expected",
        [
            ("status", "Hello word! #Image #Plone http://nohost/plone/an-image"),
            ("spoiler_text", "A Random Image"),
        ],
    )
    def test_payload_interpolation(self, mastodon_action, key: str, expected: str):
        ex = getMultiAdapter(
            (self.portal, mastodon_action, DummyEvent(self.image)), IExecutable
        )
        payload = ex._prepare_payload()
        assert payload[key] == expected

    def test_language_from_content(self, mastodon_action):
        mastodon_action.language = ""
        ex = getMultiAdapter(
            (self.portal, mastodon_action, DummyEvent(self.image)), IExecutable
        )
        payload = ex._prepare_payload()
        assert payload["language"] == self.image.language

    @pytest.mark.vcr(match_on=["path"])
    def test_execute(self, mastodon_action, wait_for):
        ex = getMultiAdapter(
            (self.portal, mastodon_action, DummyEvent(self.image)), IExecutable
        )
        payload = ex._prepare_payload()
        wait_for(ex._post(payload))

    @pytest.mark.vcr(match_on=["path"])
    def test_call(self, mastodon_action, wait_for):
        ex = getMultiAdapter(
            (self.portal, mastodon_action, DummyEvent(self.image)), IExecutable
        )
        assert ex() is True
