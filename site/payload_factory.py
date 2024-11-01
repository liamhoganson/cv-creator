from flask import session
import hashlib
from ..data_models.flask_form_data_models import CompiledPayload
from ..network.chatgpt import ChatGPT

class PayloadFactory():

    @staticmethod
    def remove_none_values(data):
        '''
        Recursively removes None and empty string values from the data.
        '''
        if isinstance(data, dict):
            # Remove keys where values are None or empty strings
            return {k: PayloadSanitizer.remove_none_values(v) for k, v in data.items() if v not in (None, '')}
        elif isinstance(data, list):
            # Remove items that are None or empty strings, but keep empty lists
            return [PayloadSanitizer.remove_none_values(item) for item in data if item not in (None, '')]
        else:
            return data

    @staticmethod
    def remove_non_unique_forms():
        '''
        Hashes each submitted form and removes duplicates to ensure clean data.
        '''
        for key, value in session.items():
            if isinstance(value, list):
                unique_entries = {}
                for entry in value:
                    form_hash = hashlib.sha256(str(entry).encode()).hexdigest()
                    unique_entries.setdefault(form_hash, entry)
                session[key] = list(unique_entries.values())

    @staticmethod
    def convert_session_to_payload():
        '''
        Converts session data to JSON payload.
        '''
        if session.get('csrf_token'):
            session.pop('csrf_token')
        if session.get('_permanent'):
            session.pop('_permanent')

        json_payload = CompiledPayload(**session).dict()
        json_payload = PayloadSanitizer.remove_none_values(json_payload)
        PayloadSanitizer.remove_non_unique_forms()
        return json_payload
