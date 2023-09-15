import logging

from confluent_kafka import Consumer, Producer
from environment import get_source_kafka_topic, get_target_kafka_topic
from kafka_consumer import KafkaConsumer
from settings import get_kafka_consumer_settings, get_kafka_producer_settings

from data_processor import DataProcessor

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    source_topic = get_source_kafka_topic()
    target_topic = get_target_kafka_topic()

    consumer_settings = get_kafka_consumer_settings()
    producer_settings = get_kafka_producer_settings()

    processor = DataProcessor(
        Producer(producer_settings),
        target_topic,
    )

    consumer = KafkaConsumer(
        source_topic,
        Consumer(consumer_settings),
        processor.process,
    )

    consumer.consume()