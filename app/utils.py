import json

import pydantic
from pydantic import BaseModel


def valid_schema_data_or_error(raw_data: dict, SchemaModel: BaseModel):
    """ этот метод проверяет валидны ли данные, отталкиваясь от схемы которую получил """
    data = {}
    errors = []
    error_str = None
    try:
        cleaned_data = SchemaModel(**raw_data)
        data = cleaned_data.dict()
    except pydantic.ValidationError as e:
        error_str = e.json()
    if error_str is not None:
        try:
            errors = json.loads(error_str)
        except Exception as e:
            errors = [{"loc": "non_field_error", "msg": "Unknown error"}]
    return data, errors