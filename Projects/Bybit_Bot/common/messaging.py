import redis.asyncio as redis
import json
import logging

logger = logging.getLogger("Messaging")

class RedisStreamManager:
    """
    Абстракция над Redis Streams для асинхронного обмена сообщениями.
    """
    def __init__(self, redis_url):
        self.redis = redis.from_url(redis_url)

    async def produce(self, stream_name, message_dict):
        """Отправка сообщения в поток"""
        try:
            # Превращаем dict в JSON для универсальности
            payload = {"data": json.dumps(message_dict)}
            await self.redis.xadd(stream_name, payload)
        except Exception as e:
            logger.error(f"Failed to produce to {stream_name}: {e}")

    async def consume(self, stream_name, group_name, consumer_name):
        """Чтение сообщений из потока (Consumer Group)"""
        try:
            # Создаем группу, если не существует
            try:
                await self.redis.xgroup_create(stream_name, group_name, mkstream=True)
            except redis.exceptions.ResponseError:
                pass # Already exists

            while True:
                # Читаем новые сообщения
                streams_dict = {stream_name: ">"}
                messages = await self.redis.xreadgroup(
                    group_name, consumer_name, streams_dict,
                    count=1, block=5000
                )
                for stream, msg_list in messages:
                    for msg_id, payload in msg_list:
                        data = json.loads(payload[b'data'])
                        yield msg_id, data
                        # Подтверждаем получение
                        await self.redis.xack(stream_name, group_name, msg_id)
        except Exception as e:
            logger.error(f"Error consuming from {stream_name}: {e}")
