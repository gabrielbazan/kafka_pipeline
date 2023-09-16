import logging
from typing import Dict, Optional, Tuple

from confluent_kafka import Consumer, Message
from settings import KAFKA_MESSAGE_ENCODING
from step import Step


class KafkaConsumerBuilder:
    @staticmethod
    def build(
        consumer_settings: Dict[str, str],
        source_topic: str,
        next_step: Step,
    ) -> "KafkaConsumer":
        return KafkaConsumer(
            Consumer(consumer_settings),
            source_topic,
            next_step,
        )


class KafkaConsumer(Step):
    def __init__(
        self,
        consumer: Consumer,
        source_topic: str,
        next_step: Optional[Step] = None,
    ) -> None:
        self.consumer: Consumer = consumer
        self.source_topic: str = source_topic
        super().__init__(next_step)

    def consume(self):
        try:
            self.try_to_consume_topic()
        except KeyboardInterrupt:
            logging.warning("Stopping consumer as requested by user")
        except Exception:
            logging.exception("Failed to consume topic '%s'", self.source_topic)
        finally:
            self.consumer.close()

    def try_to_consume_topic(self):
        self.consumer.subscribe([self.source_topic])

        while True:
            message = self.consumer.poll(timeout=1.0)

            if message is None:
                continue

            if message.error():
                logging.error(
                    "An error occurred while reading message: %s", message.error()
                )
                continue

            self(message)

    def process(self, message: Message) -> Tuple:
        return (message.value().decode(KAFKA_MESSAGE_ENCODING),)
