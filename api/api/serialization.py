import json
from typing import Any, Type

from flask import Response, jsonify
from pydantic import BaseModel, ValidationError
from settings import (
    RESPONSE_MESSAGE_KEY,
    RESPONSE_VALIDATION_ERRORS_KEY,
    RESPONSE_VALIDATION_ERRORS_MESSAGE,
)
from werkzeug.exceptions import BadRequest, InternalServerError


def to_model(model_class: Type[BaseModel], data: Any) -> BaseModel:
    try:
        return model_class(**data)
    except ValidationError as validation_error:
        response = build_schema_validation_error_response(validation_error)
        raise BadRequest(response=response)
    except Exception:
        raise InternalServerError()


def build_schema_validation_error_response(error: ValidationError) -> Response:
    errors_str = error.json()
    errors_dict = json.loads(errors_str)

    body = {
        RESPONSE_MESSAGE_KEY: RESPONSE_VALIDATION_ERRORS_MESSAGE,
        RESPONSE_VALIDATION_ERRORS_KEY: errors_dict,
    }

    response = jsonify(body)
    response.status_code = 400

    return response
