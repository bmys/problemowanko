import asyncio

from uuid import uuid1
import socket

import aio_pika
from aio_pika.pool import Pool

from cached_property import cached_property
from .service import Service
from micron import decorators


class Micron(Service):

    def __init__(self, url="amqp://guest:guest@localhost/"):
        self.id = uuid1()
        self.ip = socket.gethostbyname(socket.gethostname())
        self.url = url

        self.loop = asyncio.get_event_loop()
        self.publisher = decorators.Publisher(self)
        self.consumer = decorators.Consumer(self)
        self.tasks = list()
        self.running = False

    async def get_connection(self) -> aio_pika.connection.ConnectionType:
        return await aio_pika.connect_robust(self.url)

    async def get_channel(self) -> aio_pika.Channel:
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()

    @cached_property
    def connection_pool(self):
        return Pool(self.get_connection, max_size=2, loop=self.loop)

    @cached_property
    def channel_pool(self):
        return Pool(self.get_channel, max_size=10, loop=self.loop)

    async def main(self):
        @self.publisher('pool_queue')
        async def heart_beat():
            while self.running:
                await asyncio.sleep(10)
                await self.publisher.publish('pool_queue', "HEARTH BEAT")
            return "KILLED"

        @self.publisher('pool_queue')
        async def send_beat():
            await asyncio.sleep(1)
            return 'I AM ALIVE'

        async with self.connection_pool, self.channel_pool:
            tasks = [self.loop.create_task(task()) for task in self.tasks]
            await asyncio.wait(tasks)

    def run(self):
        self.running = True
        print(f'Micron[{str(self.id)[-8:]}] running...')
        loop = asyncio.get_event_loop()
        loop.create_task(self.main())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            ...
        finally:
            loop.close()
