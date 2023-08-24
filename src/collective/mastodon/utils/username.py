from urllib.parse import urlparse


def mastodon_username(instance: str, user: str) -> str:
    """Format username from instance information and user."""
    parsed = urlparse(instance)
    hostname = parsed.hostname
    return f"@{user}@{hostname}"
