from os import environ


class EnvironmentVariable:
    KAFKA_HOST = "KAFKA_HOST"
    KAFKA_PORT = "KAFKA_PORT"
    SOURCE_KAFKA_TOPIC = "SOURCE_KAFKA_TOPIC"
    TARGET_KAFKA_TOPIC = "TARGET_KAFKA_TOPIC"


def get_kafka_host():
    return environ[EnvironmentVariable.KAFKA_HOST]


def get_kafka_port():
    return environ[EnvironmentVariable.KAFKA_PORT]


def get_source_kafka_topic():
    return environ[EnvironmentVariable.SOURCE_KAFKA_TOPIC]


def get_target_kafka_topic():
    return environ[EnvironmentVariable.TARGET_KAFKA_TOPIC]
