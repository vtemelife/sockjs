import logging
from datetime import timedelta

import sockjs
from aiohttp import web
from sockjs.session import SessionManager

from core import settings

logger = logging.getLogger(__name__)


class SockJsListener:
    SHUTDOWN_TIMEOUT = 5

    def __init__(self, loop, handler_cls, shared_data=None, host=None, port=None):
        self.loop = loop
        self.host = host or settings.HOST
        self.port = port or settings.PORT

        app = web.Application(loop=self.loop, debug=settings.DEBUG)
        self.app = self.setup_app(app)

        self.handler = handler_cls(self.app, shared_data=shared_data)

        async def _handler_coro():
            self.app_handler = self.app.make_handler(max_line_size=settings.MAX_LINE_SIZE)

        self.app.loop.run_until_complete(_handler_coro())

    def setup_app(self, app):
        manager = SessionManager(
            "sockjs", app, self.handle, self.loop, timeout=timedelta(seconds=settings.SESSION_LIFE)
        )
        sockjs.add_endpoint(app, self.handle, name="sockjs", prefix="/sockjs/{pk}/", manager=manager)
        return app

    def get_app(self):
        return self.app

    def get_app_handler(self):
        return self.app_handler

    async def listen(self):
        return await self.loop.create_server(self.app_handler, settings.HOST, settings.PORT)

    async def handle(self, *args, **kwargs):
        return await self.handler.handle(*args, **kwargs)

    async def close(self):
        try:
            try:
                await self.app.shutdown()
                await self.app_handler.shutdown(self.SHUTDOWN_TIMEOUT)
            finally:
                await self.app.cleanup()
        except BaseException as exc:
            logger.exception(exc, exc_info=exc)
