import html
import nh3
from flask import request, jsonify, make_response, render_template
from pydantic import BaseModel, ValidationError
from typing import Iterator, Union, List
from ..data_models.flask_form_data_models import *
from .model_resolver import ModelResolver

class Validator:
    """
    Validates fields one by one, yielding any ValidationErrors encountered.
    This allows immediate error handling as soon as any validation fails.

    Args:
        data_dict: Dictionary containing data to validate
        data_model: The Pydantic model to validate against
    """

    def __init__(self, data_dict: dict, data_model: BaseModel):
        self.data_dict = data_dict
        self.data_model = data_model

    def validate_selected_fields_from_model(self) -> Iterator[ValidationError]:
        '''
        Generator to catch validation errors and yield them. Manually uses Pydantic's built in methods.
        '''
        for k, v in self.data_dict.items():
            try:
                self.data_model.__pydantic_validator__.validate_assignment(
                    self.data_model.model_construct(), k, v
                )
            except ValidationError as e:
                yield e

    @staticmethod
    def consume():
        # Extract form data from the request
        field_name: str = request.form.get("field_name")
        field_value: str = nh3.clean(request.form.get("field_value")) ## Sanitizes user input in case of HTML or JS.

        custom_errors: dict = {
            "full_name": "Please enter a valid name.",
            "phone_number": "Please enter a valid phone number.",
            "email": "Please enter a valid E-mail address.",
            "linkedin": "Please enter a valid LinkedIn URL.",
            "github": "Please enter a valid Github URL"
        }
        error: str = custom_errors.get(field_name)

        # Resolve the appropriate Pydantic model
        data_model: ModelResolver = ModelResolver().fetch_model(field_name)
        data_dict: dict = {field_name: field_value}

        # Instantiate the validator and perform validation
        validator: Validator = Validator(data_dict, data_model)
        errors: Union[List, bool] = list(validator.validate_selected_fields_from_model()) # Validator yielded errors. Returns list of errors or false.
        input_class: str = "is-danger" if errors else "is-success"

        return make_response(render_template(
            "input_field.html",
            field_name=field_name,
            sanitized_value=field_value,
            placeholder=error if errors else "",
            input_class=input_class
        ), 200)
