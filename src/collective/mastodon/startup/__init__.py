from logging import Logger


def register_apps(logger: Logger):
    """Register Mastodon apps as utilities."""
    from collective.mastodon.app import MastodonApp
    from collective.mastodon.interfaces import IMastodonApp
    from collective.mastodon.interfaces import MastodonAppInfo
    from collective.mastodon.settings import get_mastodon_apps
    from zope.component import getGlobalSiteManager

    apps_info = []
    for payload in get_mastodon_apps():
        try:
            app = MastodonAppInfo(**payload)
        except TypeError as exc:
            logger.warning(f"Wrong format for AppInfo {exc.args}")
        else:
            apps_info.append(app)
    for info in apps_info:
        app = MastodonApp(
            name=info.name, instance=info.instance, token=info.token, user=info.user
        )
        getGlobalSiteManager().registerUtility(app, IMastodonApp, name=info.name)
