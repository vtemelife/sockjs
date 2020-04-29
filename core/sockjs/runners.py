import asyncio

from core.queue.listeners import QueueListener
from core.sockjs.handlers import QueueHandler, SockJsHandler
from core.sockjs.listeners import SockJsListener


class SockJsRunner:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.shared_data = {"users": {}}
        self.sockjs_listener = SockJsListener(self.loop, SockJsHandler, shared_data=self.shared_data)
        self.app = self.sockjs_listener.get_app()
        self.app_handler = self.sockjs_listener.get_app_handler()
        self.chat_queue_listener = QueueListener(self.app, QueueHandler, "chat_queue", shared_data=self.shared_data)
        self.notification_queue_listener = QueueListener(
            self.app, QueueHandler, "notification_queue", shared_data=self.shared_data
        )

    async def listen(self):
        done, pending = await asyncio.wait(
            [
                asyncio.ensure_future(self.sockjs_listener.listen()),
                asyncio.ensure_future(self.chat_queue_listener.listen()),
                asyncio.ensure_future(self.notification_queue_listener.listen()),
            ],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

    def run(self):
        srv = self.loop.run_until_complete(self.listen())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            if self.app_handler:
                srv.close()
