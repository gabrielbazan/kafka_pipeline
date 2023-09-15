from os import environ


class EnvironmentVariable:
    API_HOST = "API_HOST"
    API_PORT = "API_PORT"
    KAFKA_HOST = "KAFKA_HOST"
    KAFKA_PORT = "KAFKA_PORT"
    KAFKA_TOPIC = "KAFKA_TOPIC"


def get_api_host():
    return environ[EnvironmentVariable.API_HOST]


def get_api_port():
    return int(environ[EnvironmentVariable.API_PORT])


def get_kafka_host():
    return environ[EnvironmentVariable.KAFKA_HOST]


def get_kafka_port():
    return environ[EnvironmentVariable.KAFKA_PORT]


def get_kafka_topic():
    return environ[EnvironmentVariable.KAFKA_TOPIC]
