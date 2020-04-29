import json
import logging

import sockjs

from core import settings
from core.queue.senders import QueueSender
from core.sockjs.senders import SockJsSender

logger = logging.getLogger(__name__)


class QueueHandler:
    def __init__(self, app, shared_data=None):
        self.app = app
        self.shared_data = shared_data
        self.sockjs_sender = SockJsSender(app, shared_data=shared_data)

    async def handle(self, encoded_message, properties):
        logger.debug(f"queue message recieve: {encoded_message}")
        message = json.loads(encoded_message.decode())
        await self.sockjs_sender.publish(message)


class SockJsHandler:
    def __init__(self, app, shared_data=None):
        self.app = app
        self.shared_data = shared_data
        self.queue_sender = QueueSender(app.loop, settings.AMQP_URL)

    def get_queue(self, message_data):
        service = message_data.get("service")
        if service == "chat":
            return "chat_queue"
        elif service == "notification":
            return "notification_queue"

    async def handle(self, sockjs_message, session):
        logger.debug(f"sockjs message recieve: {sockjs_message}")
        if sockjs_message.type == sockjs.MSG_OPEN:
            user_pk = session.request.match_info.get("pk")
            self.shared_data["users"][user_pk] = session.id
        elif sockjs_message.type == sockjs.MSG_CLOSED:
            user_pk = session.request.match_info.get("pk")
            self.shared_data["users"].pop(user_pk, None)
        elif sockjs_message.type == sockjs.MSG_MESSAGE:
            message_data = json.loads(sockjs_message.data)
            queue = self.get_queue(message_data)
            encoded_message = json.dumps(
                {"socket_id": session.id, "type": sockjs_message.type, "data": message_data}
            ).encode()
            if not queue:
                logger.error(f"no queue for: {encoded_message}")
                return
            await self.queue_sender.publish(encoded_message, queue)
