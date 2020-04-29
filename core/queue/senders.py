import logging

from aioamqp_consumer import Producer

logger = logging.getLogger(__name__)


class QueueSender:
    def __init__(self, loop, url, amqp_kwargs=None):
        self.loop = loop
        self.url = url
        self.amqp_kwargs = amqp_kwargs or {}
        self.producer = Producer(self.url, amqp_kwargs=self.amqp_kwargs, loop=self.loop)

    async def publish(self, payload, queue, queue_kwargs=None):
        if queue_kwargs is None:
            queue_kwargs = {"durable": True}

        await self.producer.publish(payload, queue, queue_kwargs=queue_kwargs)
        logger.debug(f"queue message sent: {payload}")
