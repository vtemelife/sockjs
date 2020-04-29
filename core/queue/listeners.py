import logging

from aioamqp_consumer import Consumer

from core import settings

logger = logging.getLogger(__name__)


class QueueListener:
    CONCURRENCY = 1

    def __init__(self, app, handler_cls, queue, shared_data=None):
        self.app = app
        self.queue = queue
        self.handler = handler_cls(self.app, shared_data=shared_data)
        self.consumer = None

    async def listen(self):
        url = settings.AMQP_URL
        amqp_kwargs = {}
        queue_kwargs = {"durable": True}

        self.consumer = Consumer(
            url,
            self.handle,
            self.queue,
            queue_kwargs=queue_kwargs,
            amqp_kwargs=amqp_kwargs,
            loop=self.app.loop,
            concurrency=self.CONCURRENCY,
        )
        await self.consumer.scale(20)

    async def close(self):
        try:
            self.consumer.close()
        except BaseException as exc:
            logger.exception(exc, exc_info=exc)

        try:
            await self.consumer.join()
        except BaseException as exc:
            logger.exception(exc, exc_info=exc)

        try:
            await self.consumer.wait_closed()
        except BaseException as exc:
            logger.exception(exc, exc_info=exc)

    async def handle(self, *args, **kwargs):
        await self.handler.handle(*args, **kwargs)
