from os import environ


class EnvironmentVariable:
    KAFKA_HOST = "KAFKA_HOST"
    KAFKA_PORT = "KAFKA_PORT"
    KAFKA_TOPIC = "KAFKA_TOPIC"


def get_kafka_host():
    return environ[EnvironmentVariable.KAFKA_HOST]


def get_kafka_port():
    return environ[EnvironmentVariable.KAFKA_PORT]


def get_kafka_topic():
    return environ[EnvironmentVariable.KAFKA_TOPIC]
