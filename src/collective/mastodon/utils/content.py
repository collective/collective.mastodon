from Acquisition import aq_base
from collective.mastodon.interfaces import MastodonMedia
from datetime import datetime
from DateTime import DateTime
from io import BytesIO
from plone.dexterity.content import DexterityContent
from typing import Optional
from typing import Union


__all__ = ["media_from_content", "schedule_date"]


IMAGE_ORDER = [
    ("opengraph_image_link", "image_caption", "relation"),
    ("opengraph_image", "image_caption", "field"),
    ("preview_image_link", "preview_caption_link", "relation"),
    ("preview_image", "preview_caption", "field"),
    ("image_link", "image_caption", "relation"),
    ("image", "image_caption", "field"),
]


def media_from_content(content: DexterityContent) -> Union[MastodonMedia, None]:
    """Parse a content item and return a MastodonMedia object."""
    content = aq_base(content)
    for field_name, field_caption, field_type in IMAGE_ORDER:
        title = content.title
        description = content.description
        # Image does not have an attribute image_caption
        if content.portal_type == "Image":
            caption = description
        else:
            caption = getattr(content, field_caption, None)
        field = getattr(content, field_name, None)
        if not field:
            continue
        if field_type == "relation":
            target = field.to_object
            field = target.image
            caption = caption if caption else (target.description or target.title)
        data = field.data
        if data:
            caption = caption if caption else title
            return MastodonMedia(
                file=BytesIO(data), mime_type=field.contentType, description=caption
            )


def _schedule_at(date: Optional[Union[DateTime, datetime]]) -> Union[datetime, None]:
    schedule_at = None
    if isinstance(date, DateTime) and date.isFuture():
        schedule_at = date.asdatetime()
    elif isinstance(date, datetime):
        now = datetime.now(date.tzinfo)
        if date > now:
            schedule_at = date
    return schedule_at


def schedule_date(content: DexterityContent) -> Union[datetime, None]:
    """Extract from content the date to schedule the post."""
    return _schedule_at(content.effective_date)
