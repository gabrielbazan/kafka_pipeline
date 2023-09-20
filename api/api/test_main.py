import sys
from os import environ
from os.path import dirname
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

sys.path.append(dirname(__file__))

from main import app  # noqa: E402
from settings import RAW_DATA_PATH  # noqa: E402

client = TestClient(app)


KAFKA_TOPIC = "topic_name"


MOCKED_ENVIRONMENT_VARIABLES = {
    "API_HOST": "",
    "API_PORT": "",
    "KAFKA_HOST": "",
    "KAFKA_PORT": "",
    "KAFKA_TOPIC": KAFKA_TOPIC,
}


@patch("main.Producer")
@patch.dict(environ, MOCKED_ENVIRONMENT_VARIABLES, clear=True)
def test_send_valid_raw_data(producer_mock: MagicMock) -> None:
    raw_data = {
        "timestamp": "2017-07-30T00:31:46.575000",
        "lat": 50.701,
        "long": -73.916,
        "user_id": "a1",
    }

    response = client.post(RAW_DATA_PATH, json=raw_data)

    assert response.status_code == 201
    assert response.json() == raw_data
