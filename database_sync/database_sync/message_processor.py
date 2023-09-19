import json
import logging
from abc import ABC, abstractmethod

from pymongo import MongoClient


class MessageProcessor(ABC):
    @abstractmethod
    def process(self, message: str) -> None:
        pass


class MongoDbPopulator(MessageProcessor):
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

    def process(self, message: str) -> None:
        logging.info("Processing message: %s", message)

        record = json.loads(message)

        inserted_identifier = self.sync_to_database(record)

        logging.info("Inserted record with ID %s", inserted_identifier)

    def sync_to_database(self, record):
        client = MongoClient(self.mongodb_host, self.mongodb_port)
        database = client[self.mongodb_database]
        collection = database[self.mongodb_collection]
        # TODO: if exists, then update
        return collection.insert_one(record).inserted_id
