from typing import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import Provider, Scope, from_context, provide

from pupa.config import AppConfig


class BotProvider(Provider):
	scope = Scope.APP

	config = from_context(AppConfig)

	@provide
	async def get_bot(self, config: AppConfig) -> AsyncIterable[Bot]:
		async with Bot(
			token=config.tg.token,
			default=DefaultBotProperties(parse_mode=ParseMode.HTML),
		) as bot:
			yield bot