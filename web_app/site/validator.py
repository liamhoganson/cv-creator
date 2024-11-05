from flask import request, jsonify, render_template
from pydantic import BaseModel, ValidationError
from typing import Iterator
from ..data_models.flask_form_data_models import *

class Validator:
    """
    Validates fields one by one, yielding any ValidationErrors encountered.
    This allows immediate error handling as soon as any validation fails.

    Args:
        data_dict: Dictionary containing data to validate
        data_model: The Pydantic model to validate against

    Yields:
        ValidationError: Any validation errors encountered during the process
        """

    def __init__(self, data_dict: dict, data_model: BaseModel):
        self.data_dict = data_dict
        self.data_model = data_model

    def validate_selected_fields_from_model(self) -> Iterator[ValidationError]:
        '''
        Generator to catch validation errors and yield them. Credit to: https://github.com/pydantic/pydantic/discussions/7367#discussioncomment-8969488 for the solution.
        '''
        for k, v in self.data_dict.items():
            try:
                self.data_model.__pydantic_validator__.validate_assignment(self.data_model.model_construct(), k, v)
            except ValidationError as e:
                yield e

    @staticmethod
    def consume():

        # Maps all field_names in app to respective data model that they belong to. There's probably a better way to do this. Might look into pathlib.
        #TODO: Look into pathlib for dynamically finding and loading in the respective data model for any of the field names.
        FIELD_MODEL_MAP = {
        "full_name": UserDataModel,
        "phone_number": UserDataModel,
        "email": UserDataModel,
        "linkedin": UserDataModel,
        "github": UserDataModel
        }

        field_name = request.form.get("field_name")
        field_value = request.form.get("field_value")

        if field_name not in FIELD_MODEL_MAP:
            return render_template("500.html")

        data_model = FIELD_MODEL_MAP[field_name]
        data_dict = {field_name: field_value}

        # Instantiate the validator and perform validation
        validator = Validator(data_dict, data_model)
        errors = list(validator.validate_selected_fields_from_model())

        # Log errors if they exist
        if errors:
            error_messages = [str(error) for error in errors]
            print(f"Validation Errors: {error_messages}")
            return "Could not validate!", 400

        # Successful validation
        return "Validated", 200
