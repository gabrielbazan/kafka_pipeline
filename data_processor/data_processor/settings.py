from typing import Dict

from environment import get_kafka_host, get_kafka_port

KAFKA_MESSAGE_ENCODING = "utf-8"


USER_ID_KEY = "user_id"
LATITUDE_KEY = "lat"
LONGITUDE_KEY = "long"

TIMEZONE_KEY = "timezone"


def get_kafka_consumer_settings() -> Dict[str, str]:
    return {
        "bootstrap.servers": f"{get_kafka_host()}:{get_kafka_port()}",
        "group.id": "data_processors",
        "auto.offset.reset": "earliest",
    }


def get_kafka_producer_settings() -> Dict[str, str]:
    return {
        "bootstrap.servers": f"{get_kafka_host()}:{get_kafka_port()}",
    }
