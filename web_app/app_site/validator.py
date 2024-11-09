from flask import request, jsonify, make_response
from pydantic import BaseModel, ValidationError
from typing import Iterator
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
        Generator to catch validation errors and yield them.
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
        field_name = request.form.get("field_name")
        field_value = request.form.get("field_value")

        # Resolve the appropriate Pydantic model
        data_model: BaseModel = ModelResolver().fetch_model(field_name)
        data_dict: dict = {field_name: field_value}

        # Instantiate the validator and perform validation
        validator = Validator(data_dict, data_model)
        errors = list(validator.validate_selected_fields_from_model())

        # Check for validation errors
        if errors:
            input_html = f'''
            <input class="input is-danger"
                type="text"
                name="{field_name}"
                id="{field_name}"
                placeholder="Please enter a valid phone number."
                value="{field_value}"
                hx-post="/validate"
                hx-trigger="blur"
                hx-target="#{field_name}"
                hx-swap="outerHTML"
                onblur="this.setAttribute('hx-vals', JSON.stringify({{field_name: '{field_name}', field_value: this.value}}))"/>
                '''
            return make_response(input_html, 200)

        input_html = f'''
        <input class="input is-success"
            type="text"
            name="{field_name}"
            id="{field_name}"
            placeholder="Enter Phone Number"
            value="{field_value}"
            hx-post="/validate"
            hx-trigger="blur"
            hx-target="#{field_name}"
            hx-swap="outerHTML"
            onblur="this.setAttribute('hx-vals', JSON.stringify({{field_name: '{field_name}', field_value: this.value}}))"/>
        '''
        return make_response(input_html, 200)
