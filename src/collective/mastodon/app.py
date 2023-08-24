from collective.mastodon import logger
from collective.mastodon.interfaces import IMastodonApp
from collective.mastodon.interfaces import MastodonMedia
from datetime import datetime
from mastodon import Mastodon
from threading import Thread
from typing import List
from zope.interface import implementer


USER_AGENT = "collective.mastodon"


@implementer(IMastodonApp)
class MastodonApp:
    """Mastodon App"""

    _app: Mastodon
    name: str
    instance: str
    user: str

    def __init__(self, name: str, instance: str, token: str, user: str):
        self.name = name
        self.instance = instance
        self.user = user
        self._app = Mastodon(
            access_token=token, api_base_url=instance, user_agent=USER_AGENT
        )
        self.thread_name = f"MastodonApp-Thread-{instance}-{name}"

    def status_post(
        self,
        status: str,
        media_list: List[MastodonMedia] = None,
        sensitive: bool = False,
        visibility: str = "public",
        spoiler_text: str = None,
        language: str = None,
        idempotency_key: str = None,
        scheduled_at: datetime = None,
    ) -> Thread:
        """Post a status to a Mastodon instance (using thread)."""
        payload = {
            "status": status,
            "media_list": media_list if media_list else [],
            "sensitive": sensitive,
            "visibility": visibility,
            "spoiler_text": spoiler_text,
            "language": language,
            "idempotency_key": idempotency_key,
            "scheduled_at": scheduled_at,
        }
        name = self.thread_name
        name = f"{name}-{idempotency_key}" if idempotency_key else name
        thread = Thread(
            target=self._status_post,
            name=name,
            kwargs=payload,
        )

        thread.start()
        return thread

    def _status_post(self, **payload) -> dict:
        """Post a status to a Mastodon instance and return the response."""
        app = self._app
        media_ids = []
        media_list = payload.get("media_list", [])
        if media_list:
            for media in media_list:
                response = app.media_post(
                    media.file,
                    mime_type=media.mime_type,
                    description=media.description,
                    focus=None,
                )
                media_ids.append(response["id"])
        # Prepare payload for post
        del payload["media_list"]
        payload["media_ids"] = media_ids
        post = app.status_post(**payload)
        scheduled_at = post.get("scheduled_at", None)
        if scheduled_at:
            logger.info(f"Scheduled status for {scheduled_at}")
        else:
            visibility = post["visibility"]
            url = post["url"]
            logger.info(f"Posted {visibility} status {url}")
        return post

    def scheduled_statuses(self):
        """Return a list of scheduled statuses."""
        return self._app.scheduled_statuses()
