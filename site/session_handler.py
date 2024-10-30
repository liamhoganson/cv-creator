from flask import session

class SessionHandler():

    @staticmethod
    def get_form_data(form: dict) -> dict:
        """
        Extracts data from a WTForms form instance and returns it as a dictionary.
        """
        data = {}
        for key, value in form.items():
            if value is not None:
                data.update({key: value})
        return data

    @classmethod
    def update_session(cls, session_key: str, form_data: dict, is_multiple: bool) -> dict:
        """
        Updates the session with form data.
        """
        # Adds form entry dict to a list
        if is_multiple:
            if session_key in session:
                session[session_key].append(form_data)
            else:
                session[session_key] = [form_data]
        else: # Adds form entry as a single dict object
            session.update({session_key: form_data})
        return session
