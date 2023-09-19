import json
import logging
from typing import Any, Dict

from confluent_kafka import Producer
from settings import KAFKA_MESSAGE_ENCODING


class KafkaProducerBuilder:
    @staticmethod
    def build(
        producer_settings: Dict[str, str],
        target_topic: str,
    ) -> "KafkaProducer":
        return KafkaProducer(
            Producer(producer_settings),
            target_topic,
        )


class KafkaProducer:
    def __init__(self, producer: Producer, target_topic: str) -> None:
        self.producer: Producer = producer
        self.target_topic: str = target_topic

    def produce(self, message_key: str, data: Dict[str, Any]) -> None:
        encoded_data = KafkaProducer.encode_message(data)

        logging.info(
            "Sending message with key '%s' to topic '%s'",
            message_key,
            self.target_topic,
        )

        self.producer.produce(
            topic=self.target_topic,
            key=message_key,
            value=encoded_data,
            on_delivery=KafkaProducer._produce_receipt,
        )

        self.producer.flush()

    @staticmethod
    def encode_message(data: Dict[str, Any]) -> bytes:
        data_str = json.dumps(data)
        return data_str.encode(KAFKA_MESSAGE_ENCODING)

    @staticmethod
    def _produce_receipt(error, message):
        if error is not None:
            logging.error(
                "An error occurred while sending the message to the topic: '%s'", error
            )
        else:
            message_value = message.value().decode(KAFKA_MESSAGE_ENCODING)

            logging.info(
                "Sent message to partition '%s' of topic '%s'. Value: %s",
                message.partition(),
                message.topic(),
                message_value,
            )
