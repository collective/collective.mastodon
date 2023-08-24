from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import collective.mastodon


class MastodonLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.restapi
        import plone.volto

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=plone.volto)
        self.loadZCML(package=collective.mastodon)

    def setUpPloneSite(self, portal):
        st = portal.portal_setup
        st.runAllImportStepsFromProfile("plone.volto:default")


FIXTURE = MastodonLayer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="MastodonLayer:IntegrationTesting",
)
