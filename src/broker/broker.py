from faststream.rabbit import RabbitBroker, RabbitQueue
from src.app.settings.settings import config

broker = RabbitBroker(config.broker_url)

payments_queue = RabbitQueue(
    config.payment_topic,
    durable=True,
    arguments={
        "x-dead-letter-exchange": "",
        "x-dead-letter-routing-key": config.payment_dlq_topic,
    })
payments_dlq_queue = RabbitQueue(config.payment_dlq_topic)