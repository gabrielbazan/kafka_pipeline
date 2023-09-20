import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

from kafka_producer import KafkaProducer
from settings import LATITUDE_KEY, LONGITUDE_KEY, TIMEZONE_KEY, USER_ID_KEY
from time_zone import get_timezone


class MessageProcessor(ABC):
    @abstractmethod
    def process(self, message: str) -> None:
        pass


class TimezoneAppender(MessageProcessor):
    def __init__(self, kafka_producer: KafkaProducer) -> None:
        self.kafka_producer: KafkaProducer = kafka_producer

    def process(self, message: str) -> None:
        logging.info("Processing message: %s", message)

        user_id, data = TimezoneAppender.process_message(message)

        self.kafka_producer.produce(user_id, data)

    @staticmethod
    def process_message(message: str) -> Tuple[str, Dict[str, Any]]:
        data = TimezoneAppender.parse_message(message)

        user_id = data[USER_ID_KEY]

        TimezoneAppender.add_timezone(data)

        return user_id, data

    @staticmethod
    def parse_message(message: str) -> Dict[str, Any]:
        data: Dict[str, Any] = json.loads(message)
        return data

    @staticmethod
    def add_timezone(data: Dict[str, Any]) -> None:
        latitude = data[LATITUDE_KEY]
        longitude = data[LONGITUDE_KEY]

        data[TIMEZONE_KEY] = TimezoneAppender.try_to_get_timezone(latitude, longitude)

    @staticmethod
    def try_to_get_timezone(latitude: float, longitude: float) -> Optional[str]:
        timezone = None

        try:
            timezone = get_timezone(latitude, longitude)
        except Exception:
            logging.exception(
                "Could not determine UTC timestamp. Defaulting to original."
            )

        return timezone
