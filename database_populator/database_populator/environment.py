from os import environ


class EnvironmentVariable:
    KAFKA_HOST = "KAFKA_HOST"
    KAFKA_PORT = "KAFKA_PORT"
    KAFKA_TOPIC = "KAFKA_TOPIC"
    MONGODB_HOST = "MONGODB_HOST"
    MONGODB_PORT = "MONGODB_PORT"
    MONGODB_DATABASE = "MONGODB_DATABASE"
    MONGODB_COLLECTION = "MONGODB_COLLECTION"


def get_kafka_host():
    return environ[EnvironmentVariable.KAFKA_HOST]


def get_kafka_port():
    return environ[EnvironmentVariable.KAFKA_PORT]


def get_kafka_topic():
    return environ[EnvironmentVariable.KAFKA_TOPIC]


def get_mongodb_host():
    return environ[EnvironmentVariable.MONGODB_HOST]


def get_mongodb_port():
    return int(environ[EnvironmentVariable.MONGODB_PORT])


def get_mongodb_database():
    return environ[EnvironmentVariable.MONGODB_DATABASE]


def get_mongodb_collection():
    return environ[EnvironmentVariable.MONGODB_COLLECTION]
