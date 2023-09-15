import json
import logging
from typing import Any, Callable, Dict, Tuple

from confluent_kafka import Message
from settings import (
    KAFKA_MESSAGE_ENCODING,
    LATITUDE_KEY,
    LONGITUDE_KEY,
    TIMEZONE_KEY,
    USER_ID_KEY,
)
from time_zone import get_timezone


class DataProcessor:
    def __init__(self, on_processed: Callable) -> None:
        self.on_processed: Callable = on_processed

    def process(self, message):
        text_data = DataProcessor.decode_message(message)

        logging.info("Processing message: %s", text_data)

        user_id, data = DataProcessor.process_message(text_data)

        self.invoke_next_step(user_id, data)

    @staticmethod
    def decode_message(message: Message) -> str:
        return message.value().decode(KAFKA_MESSAGE_ENCODING)

    @staticmethod
    def process_message(text_data: str) -> Tuple[str, Dict[str, Any]]:
        data = json.loads(text_data)

        user_id = data[USER_ID_KEY]
        latitude = data[LATITUDE_KEY]
        longitude = data[LONGITUDE_KEY]

        data[TIMEZONE_KEY] = DataProcessor.try_to_get_timezone(latitude, longitude)

        return user_id, data

    @staticmethod
    def try_to_get_timezone(latitude, longitude):
        try:
            return get_timezone(latitude, longitude)
        except Exception:
            logging.exception(
                "Could not determine UTC timestamp. Defaulting to original."
            )
            return None  # Making it explicit

    def invoke_next_step(self, user_id: str, data: Dict[str, Any]) -> None:
        self.on_processed(user_id, data)
