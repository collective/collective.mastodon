from prettyconf import config


def get_mastodon_apps():
    return config("MASTODON_APPS", cast=config.json, default="[]")
