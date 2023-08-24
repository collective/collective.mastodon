"""Init and utils."""
from collective.mastodon import startup
from zope.i18nmessageid import MessageFactory

import logging


PACKAGE_NAME = "collective.mastodon"

_ = MessageFactory(PACKAGE_NAME)

logger = logging.getLogger(PACKAGE_NAME)

startup.register_apps(logger)
