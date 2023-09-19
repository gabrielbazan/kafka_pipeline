import json
import logging
from typing import Any, Dict

from confluent_kafka import Producer
from settings import KAFKA_MESSAGE_ENCODING


def produce(
    producer: Producer,
    topic_name: str,
    message_key: str,
    data: Dict[str, Any],
) -> None:
    data_str = json.dumps(data)
    encoded_data_str = data_str.encode(KAFKA_MESSAGE_ENCODING)

    logging.info("Sending message with key '%s' to topic '%s'", message_key, topic_name)

    producer.produce(
        topic=topic_name,
        key=message_key,
        value=encoded_data_str,
        on_delivery=_produce_receipt,
    )
    producer.flush()


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
