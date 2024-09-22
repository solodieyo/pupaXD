from taskiq import TaskiqScheduler, TaskiqEvents
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend, RedisScheduleSource

broker = ListQueueBroker(
	"redis://localhost:6379/0",
)

redis_async_result = RedisAsyncResultBackend(
	redis_url='redis://localhost:6379',
)

broker.with_result_backend(redis_async_result)
redis_source = RedisScheduleSource('redis://localhost:6379/1')
scheduler = TaskiqScheduler(broker, [redis_source])


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup_event(context):
	pass