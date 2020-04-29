import json
import logging

logger = logging.getLogger(__name__)


class SockJsSender:
    def __init__(self, app, shared_data=None):
        self.app = app
        self.shared_data = shared_data

    def get_session(self, socket_id):
        session_manager = self.app["__sockjs_managers__"]["sockjs"]
        try:
            return session_manager.get(socket_id)
        except KeyError:
            logger.info("Session (%s) is not found", socket_id)

    async def publish(self, message):
        socket_id = message["socket_id"]
        recipients = message.get("data", {}).get("recipients")
        sockjs_message = json.dumps(message)

        if recipients is None:
            session = self.get_session(socket_id)
            if not session:
                return
            session.manager.broadcast(sockjs_message)
            return

        for recipient in recipients:
            recipient_session_id = self.shared_data["users"].get(recipient)
            session = self.get_session(recipient_session_id)
            if not session:
                continue
            session.send(sockjs_message)
