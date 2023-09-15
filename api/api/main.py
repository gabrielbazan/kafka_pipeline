import logging
from typing import Any, Dict

from confluent_kafka import Producer
from environment import get_kafka_topic
from fastapi import FastAPI
from kafka import produce
from models import RawData
from settings import (
    PYDANTIC_MODEL_DUMP_MODE,
    RAW_DATA_PATH,
    get_kafka_producer_settings,
)

logging.basicConfig(level=logging.DEBUG)


app = FastAPI()


@app.post(RAW_DATA_PATH, status_code=201)
async def ingest_raw_data(raw_data: RawData):
    model_json = raw_data.model_dump(mode=PYDANTIC_MODEL_DUMP_MODE)

    send_to_kafka(raw_data.user_id, model_json)

    return model_json


def send_to_kafka(user_id: str, data_json: Dict[str, Any]) -> None:
    kafka_topic = get_kafka_topic()
    producer_settings = get_kafka_producer_settings()
    producer = Producer(producer_settings)
    produce(producer, kafka_topic, user_id, data_json)
