import logging

from confluent_kafka import Consumer
from environment import (
    get_kafka_topic,
    get_mongodb_collection,
    get_mongodb_database,
    get_mongodb_host,
    get_mongodb_port,
)
from kafka_consumer import KafkaConsumer
from mongo_sync import MongoSync
from settings import get_kafka_consumer_settings

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    kafka_topic = get_kafka_topic()
    kafka_consumer_settings = get_kafka_consumer_settings()

    database_sync = MongoSync(
        get_mongodb_host(),
        get_mongodb_port(),
        get_mongodb_database(),
        get_mongodb_collection(),
    )

    consumer = KafkaConsumer(
        kafka_topic,
        Consumer(kafka_consumer_settings),
        database_sync.process_message,
    )

    consumer.consume()
