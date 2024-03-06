import os

import pika
from pika.adapters.blocking_connection import BlockingChannel

TOURIST_PACKAGE_QUEUE = 'tourist_packages'


class RabbitMQConnection(object):
    _instance: "RabbitMQConnection" = None
    channel: BlockingChannel = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls) -> "RabbitMQConnection":
        if cls._instance is None:
            instance: "RabbitMQConnection" = cls.__new__(cls)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(os.getenv("RABBITMQ_HOST", "127.0.0.1"), heartbeat=5000))
            instance.channel = connection.channel()
            instance.channel.queue_declare(queue=TOURIST_PACKAGE_QUEUE)
            cls._instance = instance
        if cls._instance.channel.is_closed or not cls._instance.channel.is_open:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(os.getenv("RABBITMQ_HOST", "127.0.0.1"), heartbeat=5000))
            cls._instance.channel = connection.channel()
            cls._instance.channel.queue_declare(queue=TOURIST_PACKAGE_QUEUE)
        return cls._instance
