import logging
from typing import Dict

from environment import (
    get_kafka_topic,
    get_mongodb_collection,
    get_mongodb_database,
    get_mongodb_host,
    get_mongodb_port,
)
from kafka_consumer import KafkaConsumer, KafkaConsumerBuilder
from message_processor import MessageProcessor, MongoDbPopulator
from settings import get_kafka_consumer_settings

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    source_topic: str = get_kafka_topic()
    consumer_settings: Dict[str, str] = get_kafka_consumer_settings()

    message_processor: MessageProcessor = MongoDbPopulator(
        get_mongodb_host(),
        get_mongodb_port(),
        get_mongodb_database(),
        get_mongodb_collection(),
    )

    kafka_consumer: KafkaConsumer = KafkaConsumerBuilder.build(
        consumer_settings,
        source_topic,
        message_processor,
    )

    with kafka_consumer:
        logging.info("Consuming Kafka topic")
        kafka_consumer.consume()

    logging.info("End of process")
