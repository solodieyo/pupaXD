from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from dishka import AsyncContainer

from pupa.infrastructure.db.repositories.general_repository import GeneralRepository


class UserMiddleware(BaseMiddleware):
	def __init__(self, dishka: AsyncContainer):
		super().__init__()
		self.dishka = dishka

	async def __call__(
		self,
		handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
		event: Union[Message, CallbackQuery],
		data: dict[str, Any],
	):
		async with self.dishka() as req_dishka:
			repo: GeneralRepository = await req_dishka.get(GeneralRepository)

			user, new_user = await repo.user.get_or_create_user(
				tg_user_id=event.from_user.id,
				username=event.from_user.username,
				full_name=event.from_user.full_name
			)
			pupa = await repo.pupa.get_or_create_pupa(
				owner_id=user.id
			)

			data['pupa'] = pupa
			data['user'] = user
			data['new_user'] = new_user
			return await handler(event, data)