import json
import logging
from abc import ABC, abstractmethod
from typing import Callable, Optional, Tuple

from settings import LATITUDE_KEY, LONGITUDE_KEY, TIMEZONE_KEY, USER_ID_KEY
from time_zone import get_timezone


class DataProcessor(ABC):
    def __init__(self, on_processed: Callable) -> None:
        self.on_processed: Callable = on_processed

    def process(self, message: str) -> None:
        processed_data = self._process(message)
        self._invoke_next_step(processed_data)

    @abstractmethod
    def _process(self, message: str) -> Tuple:
        pass

    def _invoke_next_step(self, processed_data: Tuple) -> None:
        self.on_processed(*processed_data)


class RawDataProcessor(DataProcessor):
    def _process(self, message: str) -> Tuple:
        logging.info("Processing message: %s", message)

        data = json.loads(message)

        user_id = data[USER_ID_KEY]
        latitude = data[LATITUDE_KEY]
        longitude = data[LONGITUDE_KEY]

        data[TIMEZONE_KEY] = RawDataProcessor.try_to_get_timezone(latitude, longitude)

        return user_id, data

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
