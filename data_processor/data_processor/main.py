import logging
from typing import Dict

from environment import get_source_kafka_topic, get_target_kafka_topic
from kafka_consumer import KafkaConsumer, KafkaConsumerBuilder
from kafka_producer import KafkaProducer, KafkaProducerBuilder
from message_processor import MessageProcessor, TimezoneAppender
from settings import get_kafka_consumer_settings, get_kafka_producer_settings

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    source_topic: str = get_source_kafka_topic()
    target_topic: str = get_target_kafka_topic()

    consumer_settings: Dict[str, str] = get_kafka_consumer_settings()
    producer_settings: Dict[str, str] = get_kafka_producer_settings()

    kafka_producer: KafkaProducer = KafkaProducerBuilder.build(
        producer_settings,
        target_topic,
    )

    message_processor: MessageProcessor = TimezoneAppender(kafka_producer)

    kafka_consumer: KafkaConsumer = KafkaConsumerBuilder.build(
        consumer_settings,
        source_topic,
        message_processor,
    )

    with kafka_consumer:
        logging.info("Consuming Kafka topic")
        kafka_consumer.consume()

    logging.info("End of process")
