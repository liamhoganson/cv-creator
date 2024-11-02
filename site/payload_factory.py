import json
import hashlib
from flask import session
from ..site.session_handler import SessionHandler
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
            return {k: PayloadFactory.remove_none_values(v) for k, v in data.items() if v not in (None, '')}
        elif isinstance(data, list):
            # Remove items that are None or empty strings, but keep empty lists
            return [PayloadFactory.remove_none_values(item) for item in data if item not in (None, '')]
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
    async def convert_session_to_payload():
        '''
        Converts session data to JSON payload.
        '''
        session_data = dict(session)
        session.pop('csrf_token', None)
        session.pop('_permanent', None)
        print(session_data)

        # AI Options
        ai_options_data = session_data.get('ai_options_data', {})
        if ai_options_data.get('add_summary'):
            summary = await ChatGPT(session_data).get_resume_summary()
            SessionHandler().update_session(session_key="summary", form_data=summary, is_multiple=False)
        if ai_options_data.get('edit_attributes'):
            ai_edited_object = await ChatGPT(session_data).edit_resume_attributes()
            print(ai_edited_object)
            session_data = json.loads(ai_edited_object)
        session_data.pop('ai_options_data', None)

        PayloadFactory.remove_non_unique_forms()
        json_payload = CompiledPayload(**session_data).dict()
        json_payload = PayloadFactory.remove_none_values(json_payload)
        return json_payload
