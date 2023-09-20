from os import environ


class EnvironmentVariable:
    KAFKA_HOST = "KAFKA_HOST"
    KAFKA_PORT = "KAFKA_PORT"
    KAFKA_TOPIC = "KAFKA_TOPIC"
    MONGODB_HOST = "MONGODB_HOST"
    MONGODB_PORT = "MONGODB_PORT"
    MONGODB_DATABASE = "MONGODB_DATABASE"
    MONGODB_COLLECTION = "MONGODB_COLLECTION"


def get_kafka_host() -> str:
    return environ[EnvironmentVariable.KAFKA_HOST]


def get_kafka_port() -> str:
    return environ[EnvironmentVariable.KAFKA_PORT]


def get_kafka_topic() -> str:
    return environ[EnvironmentVariable.KAFKA_TOPIC]


def get_mongodb_host() -> str:
    return environ[EnvironmentVariable.MONGODB_HOST]


def get_mongodb_port() -> int:
    return int(environ[EnvironmentVariable.MONGODB_PORT])


def get_mongodb_database() -> str:
    return environ[EnvironmentVariable.MONGODB_DATABASE]


def get_mongodb_collection() -> str:
    return environ[EnvironmentVariable.MONGODB_COLLECTION]
