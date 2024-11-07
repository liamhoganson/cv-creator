import json
import hashlib
from flask import session, render_template
from ..app_site.session_handler import SessionHandler
from ..data_models.flask_form_data_models import CompiledPayload
from ..network.chatgpt import ChatGPT

class PayloadFactory:

    @staticmethod
    def remove_none_values(data):
        """
        Recursively removes None and empty string values from the data.
        """
        if isinstance(data, dict):
            return {
                k: PayloadFactory.remove_none_values(v)
                for k, v in data.items()
                if v not in (None, '')
            }
        elif isinstance(data, list):
            return [
                PayloadFactory.remove_none_values(item)
                for item in data if item not in (None, '')
            ]
        return data

    @staticmethod
    def remove_non_unique_forms():
        """
        Hashes each submitted form and removes duplicates to ensure clean data.
        """
        for key, value in session.items():
            if isinstance(value, list):
                unique_entries = {
                    hashlib.sha256(str(entry).encode()).hexdigest(): entry
                    for entry in value
                }
                session[key] = list(unique_entries.values())

    @staticmethod
    async def process_ai_options(session_data: dict):
        """
        Processes AI options from the session data and updates the session accordingly.
        """
        ai_options_data = session_data.get('ai_options_data', {})
        if ai_options_data.get('add_summary'):
            summary = await ChatGPT(session_data).get_resume_summary()
            SessionHandler().update_session(session_key="summary", form_data=summary, is_multiple=False)
        if ai_options_data.get('edit_attributes'):
            ai_edited_object = await ChatGPT(session_data).edit_resume_attributes()
            return json.loads(ai_edited_object)
        return session_data

    @staticmethod
    async def convert_session_to_payload():
        """
        Converts session data to JSON payload.
        """
        session_data = dict(session)
        session_data.pop('csrf_token', None)
        session_data.pop('_permanent', None)

        try:
            session_data = await PayloadFactory.process_ai_options(session_data)
            PayloadFactory.remove_non_unique_forms()
            json_payload = CompiledPayload(**session_data).dict()
            print(PayloadFactory.remove_none_values(json_payload))
            return PayloadFactory.remove_none_values(json_payload)
        except Exception:
            return render_template('500.html')
