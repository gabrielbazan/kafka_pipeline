from typing import Any, Dict, Tuple

from confluent_kafka import Producer
from environment import get_kafka_topic
from flask import request
from flask_restful import Resource
from kafka import produce
from resources.raw_data.models import RawData
from serialization import to_model
from settings import PYDANTIC_MODEL_DUMP_MODE, get_kafka_producer_settings


class RawDataResource(Resource):
    def put(self) -> Tuple[Dict[str, Any], int]:
        model: RawData = to_model(RawData, request.json)

        model_json = self.serialize_model(model)

        self.send_to_kafka(model.user_id, model_json)

        return model_json, 200

    def serialize_model(self, model: RawData) -> Dict[str, Any]:
        return model.model_dump(mode=PYDANTIC_MODEL_DUMP_MODE)

    def send_to_kafka(self, user_id: str, data_point_json: Dict[str, Any]) -> None:
        kafka_topic = get_kafka_topic()
        producer_settings = get_kafka_producer_settings()
        producer = Producer(producer_settings)
        produce(producer, kafka_topic, user_id, data_point_json)
