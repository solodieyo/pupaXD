from dishka import Provider, Scope, provide
from taskiq_redis import RedisScheduleSource


class RedisSourceProvider(Provider):
	scope = Scope.APP

	@provide
	async def get_redis_source(self) -> RedisScheduleSource:
		return RedisScheduleSource('redis://localhost:6379/1')