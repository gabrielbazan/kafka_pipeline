import json
import logging
from typing import Any, Dict, Tuple

from confluent_kafka import Message, Producer
from kafka import produce
from settings import (
    KAFKA_MESSAGE_ENCODING,
    LATITUDE_KEY,
    LONGITUDE_KEY,
    MESSAGE_TIMESTAMP_FORMAT,
    TIMESTAMP_KEY,
    USER_ID_KEY,
)
from time_zone import to_utc


class DataProcessor:
    def __init__(self, producer: Producer, target_topic: str) -> None:
        self.producer: Producer = producer
        self.target_topic: str = target_topic

    def process(self, message):
        text_data = DataProcessor.decode_message(message)

        logging.info("Processing message: %s", text_data)

        user_id, data = DataProcessor.process_message(text_data)

        self.send_to_target_topic(user_id, data)

    @staticmethod
    def decode_message(message: Message) -> str:
        return message.value().decode(KAFKA_MESSAGE_ENCODING)

    @staticmethod
    def process_message(text_data: str) -> Tuple[str, Dict[str, Any]]:
        data = json.loads(text_data)

        user_id = data[USER_ID_KEY]
        timestamp = data[TIMESTAMP_KEY]
        latitude = data[LATITUDE_KEY]
        longitude = data[LONGITUDE_KEY]

        data[TIMESTAMP_KEY] = DataProcessor.try_to_convert_to_utc(
            timestamp,
            latitude,
            longitude,
        )

        return user_id, data

    @staticmethod
    def try_to_convert_to_utc(datetime_str, latitude, longitude):
        try:
            return to_utc(
                datetime_str,
                latitude,
                longitude,
                MESSAGE_TIMESTAMP_FORMAT,
                MESSAGE_TIMESTAMP_FORMAT,
            )
        except Exception:
            logging.exception(
                "Could not determine UTC timestamp. Defaulting to original."
            )
            return datetime_str

    def send_to_target_topic(self, user_id: str, data: Dict[str, Any]):
        produce(self.producer, self.target_topic, user_id, data)