from typing import Text
import functools

import aio_pika
from .service import Service


class Consumer:
    def __init__(self, micron: Service):
        self.service = micron

    def __call__(self, queue_name: Text):
        def actual_decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                async with self.service.channel_pool.acquire() as channel:
                    await channel.set_qos(10)
                    queue = await channel.declare_queue(queue_name, durable=False, auto_delete=False)

                    async with queue.iterator() as queue_iter:
                        async for message in queue_iter:
                            msg = message.body.decode('utf-8')
                            await func(msg, *args, **kwargs)
                            await message.ack()

            self.service.tasks.append(wrapper)
            return wrapper

        return actual_decorator


class Publisher:
    def __init__(self, micron: Service):
        self.service = micron

    async def publish(self, queue_name, msg):
        async with self.service.channel_pool.acquire() as channel:  # type: aio_pika.Channel
            await channel.default_exchange.publish(aio_pika.Message(msg.encode()), queue_name)

    def __call__(self, queue_name: Text):
        def actual_decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                if result and result != 'PASS':
                    await self.publish(queue_name, result)

            self.service.tasks.append(wrapper)
            return wrapper

        return actual_decorator
