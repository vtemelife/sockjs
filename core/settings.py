import os

AMQP_URL = os.environ["AMQP_URL"]
HOST = os.environ["SOCKJS_HOST"]
PORT = os.environ["SOCKJS_PORT"]

SESSION_LIFE = 7200
DEBUG = False
MAX_LINE_SIZE = 8190 * 10
