from dataclasses import dataclass

from aiogram.enums import ContentType
from aiogram.types import Message


@dataclass
class FileInfo:
	file_id: str | None
	content_type: ContentType | None


def get_file_info(message: Message):
	if message.photo:
		return FileInfo(message.photo[-1].file_id, ContentType.PHOTO)
	elif message.document:
		return FileInfo(message.document.file_id, ContentType.DOCUMENT)
	elif message.video:
		return FileInfo(message.video.file_id, ContentType.VIDEO)
	else:
		return FileInfo(None, None)