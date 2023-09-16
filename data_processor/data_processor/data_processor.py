import json
import logging
from typing import Optional, Tuple

from settings import LATITUDE_KEY, LONGITUDE_KEY, TIMEZONE_KEY, USER_ID_KEY
from step import Step
from time_zone import get_timezone


class DataProcessor(Step):
    def process(self, message: str) -> Tuple:
        logging.info("Processing message: %s", message)

        data = json.loads(message)

        user_id = data[USER_ID_KEY]
        latitude = data[LATITUDE_KEY]
        longitude = data[LONGITUDE_KEY]

        data[TIMEZONE_KEY] = DataProcessor.try_to_get_timezone(latitude, longitude)

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
