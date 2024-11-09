from pathlib import Path
from importlib import import_module
from pydantic import BaseModel
from flask import render_template
import inspect
import sys

class ModelResolver:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        sys.path.append(str(self.project_root))
        self.data_models_module = "data_models.flask_form_data_models"
        try:
            self.data_models = import_module(str(self.data_models_module))
        except ImportError:
            raise(f"Could not load in data models!")

    def fetch_model(self, query_string: str) -> BaseModel:
        for obj_name, obj in inspect.getmembers(self.data_models, inspect.isclass):
                if issubclass(obj, BaseModel) and obj != BaseModel:
                    if query_string in obj.model_fields.keys():
                        print(f"Found Data Model! Using: {obj_name}")
                        return obj
        raise ValueError(f"Could not find associated data model for query string: {query_string}")
