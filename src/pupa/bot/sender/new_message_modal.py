from dataclasses import dataclass
from typing import Optional

from aiogram.enums import ParseMode
from aiogram_dialog.api.entities import MarkupVariant


@dataclass
class NewMessage:
	chat_id: int
	text: Optional[str] = None
	reply_markup: Optional[MarkupVariant] = None
	parse_mode: Optional[str] = ParseMode.HTML
	disable_web_page_preview: Optional[bool] = True
	media_id: Optional[str] = None
	media_content_type: Optional[str] = None
	poll_tittle: Optional[str] = None
	poll_options: Optional[list[str]] = None
	disable_notification: Optional[bool] = True
	hide_media: Optional[bool] = False
