from environment import get_kafka_host, get_kafka_port

KAFKA_MESSAGE_ENCODING = "utf-8"


def get_kafka_consumer_settings():
    return {
        "bootstrap.servers": f"{get_kafka_host()}:{get_kafka_port()}",
        "group.id": "database_sync",
        "auto.offset.reset": "earliest",
    }
