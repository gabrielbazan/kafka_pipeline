import logging

from environment import get_api_host, get_api_port
from flask import Flask
from flask_restful import Api
from resources.raw_data.resource import RawDataResource
from settings import RAW_DATA_PATH

app = Flask(__name__)
api = Api(app)

api.add_resource(RawDataResource, RAW_DATA_PATH)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    host = get_api_host()
    port = get_api_port()

    app.run(debug=True, host=host, port=port)
