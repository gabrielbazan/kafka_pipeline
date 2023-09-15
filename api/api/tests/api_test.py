from os import environ
from unittest import TestCase
from unittest.mock import ANY, MagicMock, patch

from main import app

KAFKA_TOPIC = "topic_name"


MOCKED_ENVIRONMENT_VARIABLES = {
    "API_HOST": "",
    "API_PORT": "",
    "KAFKA_HOST": "",
    "KAFKA_PORT": "",
    "KAFKA_TOPIC": KAFKA_TOPIC,
}


@patch("resources.raw_data.resource.Producer")
class ApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    @patch.dict(environ, MOCKED_ENVIRONMENT_VARIABLES, clear=True)
    def test_should_return_200_when_data_is_valid(
        self,
        producer_class_mock: MagicMock,
    ) -> None:
        # Given
        user_id = "a1"

        data = {
            "timestamp": "2017-01-01 13:05:12",
            "lat": 40.701,
            "long": -73.916,
            "user_id": user_id,
        }

        producer_mock = MagicMock()
        producer_class_mock.return_value = producer_mock

        # When
        response = self.client.put("/raw_data", json=data)

        # Then
        producer_class_mock.assert_called_once()
        producer_mock.produce.assert_called_once_with(
            topic=KAFKA_TOPIC,
            key=user_id,
            value=ANY,
            on_delivery=ANY,
        )
        producer_mock.flush.assert_called_once_with()

        self.assertEqual(response.status_code, 200)

    @patch.dict(environ, MOCKED_ENVIRONMENT_VARIABLES, clear=True)
    def test_should_return_400_when_missing_timestamp(
        self, producer_class_mock: MagicMock
    ) -> None:
        # Given
        data = {
            "lat": 40.701,
            "long": -73.916,
            "user_id": "a1",
        }

        # When
        response = self.client.put("/raw_data", json=data)

        # Then
        producer_class_mock.assert_not_called()

        self.assertEqual(response.status_code, 400)
