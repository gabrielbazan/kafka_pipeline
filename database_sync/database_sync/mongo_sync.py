import json
import logging

from confluent_kafka import Message
from pymongo import MongoClient
from settings import KAFKA_MESSAGE_ENCODING


class MongoSync:
    def __init__(
        self,
        mongodb_host,
        mongodb_port,
        mongodb_database,
        mongodb_collection,
    ) -> None:
        self.mongodb_host = mongodb_host
        self.mongodb_port = mongodb_port
        self.mongodb_database = mongodb_database
        self.mongodb_collection = mongodb_collection

    def process_message(self, message: Message) -> None:
        data = MongoSync.decode_message(message)

        logging.info("Processing message: %s", data)

        record = json.loads(data)

        inserted_identifier = self.sync_to_database(record)

        logging.info("Inserted record with ID %s", inserted_identifier)

    @staticmethod
    def decode_message(message: Message) -> str:
        return message.value().decode(KAFKA_MESSAGE_ENCODING)

    def sync_to_database(self, record):
        client = MongoClient(self.mongodb_host, self.mongodb_port)
        database = client[self.mongodb_database]
        collection = database[self.mongodb_collection]
        # TODO: Assuming data is in chronological order
        # if exists, then update
        return collection.insert_one(record).inserted_id
