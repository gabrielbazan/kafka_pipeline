import logging
from typing import Dict

from confluent_kafka import Consumer, Message
from message_processor import MessageProcessor
from settings import KAFKA_MESSAGE_ENCODING

POLL_TIMEOUT = 1.0


class KafkaConsumerBuilder:
    @staticmethod
    def build(
        consumer_settings: Dict[str, str],
        source_topic: str,
        message_processor: MessageProcessor,
    ) -> "KafkaConsumer":
        return KafkaConsumer(
            Consumer(consumer_settings),
            source_topic,
            message_processor,
        )


class KafkaConsumer:
    def __init__(
        self,
        consumer: Consumer,
        source_topic: str,
        message_processor: MessageProcessor,
    ) -> None:
        self.consumer: Consumer = consumer
        self.source_topic: str = source_topic
        self.message_processor: MessageProcessor = message_processor

    def __enter__(self):
        self.consumer.subscribe([self.source_topic])

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.close()

    def consume(self):
        try:
            self.try_to_consume_topic()
        except KeyboardInterrupt:
            logging.warning("Stopping consumer as requested by user")
        except Exception:
            logging.exception("Failed to consume topic '%s'", self.source_topic)

    def try_to_consume_topic(self) -> None:
        while True:
            message: Message = self.consumer.poll(timeout=POLL_TIMEOUT)

            if message is None:
                continue

            error_message: str = message.error()

            if error_message:
                logging.error("Error while reading message: %s", error_message)
            else:
                self.process_message(message)

    def process_message(self, message: Message) -> None:
        try:
            self.try_to_process_message(message)
        except Exception:
            logging.exception("Error while processing message")

    def try_to_process_message(self, message: Message) -> None:
        decoded_message = self.decode_message(message)
        self.message_processor.process(decoded_message)

    @staticmethod
    def decode_message(message: Message) -> str:
        return message.value().decode(KAFKA_MESSAGE_ENCODING)
