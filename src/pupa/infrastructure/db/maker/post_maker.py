from datetime import date

from app.src.infrastructure.db.models.posts import Post


def create_post(
	data: dict,
	user_id: int,
	scheduled: bool = False,
	scheduled_at: date | None = None,
	sent: bool = True
) -> Post:
	return Post(
		channel_id=data['channel_id'],
		owner_user_id=user_id,
		text=data.get('post_text', '.'),
		notification=data.get('notification', False),
		media_id=data.get('media_id', None),
		url_buttons=data.get('url_buttons', None),
		emoji_buttons=data.get('emoji_buttons', None),
		poll_tittle=data.get('poll_tittle', None),
		poll_options=data.get('poll_options', None),
		scheduled=scheduled,
		scheduled_at=scheduled_at,
		hide_media=data.get('hide_media', False),
		media_content_type=data.get('media_content_type', None),
		sent=sent
	)