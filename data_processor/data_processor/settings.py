from environment import get_kafka_host, get_kafka_port

KAFKA_MESSAGE_ENCODING = "utf-8"

TIMESTAMP_KEY = "timestamp"
USER_ID_KEY = "user_id"
LATITUDE_KEY = "lat"
LONGITUDE_KEY = "long"

MESSAGE_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def get_kafka_consumer_settings():
    return {
        "bootstrap.servers": f"{get_kafka_host()}:{get_kafka_port()}",
        "group.id": "data_processors",
        "auto.offset.reset": "earliest",
    }


def get_kafka_producer_settings():
    return {
        "bootstrap.servers": f"{get_kafka_host()}:{get_kafka_port()}",
    }
