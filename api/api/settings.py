from environment import get_kafka_host, get_kafka_port

RAW_DATA_PATH = "/raw_data"

PYDANTIC_MODEL_DUMP_MODE = "json"

KAFKA_MESSAGE_ENCODING = "utf-8"


def get_kafka_producer_settings():
    return {
        "bootstrap.servers": f"{get_kafka_host()}:{get_kafka_port()}",
    }
