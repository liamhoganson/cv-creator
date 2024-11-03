from flask import request, redirect, url_for, render_template
from ..base_page import BasePage
from ..site.forms import UserForm
from ..site.session_handler import SessionHandler
from ..data_models.flask_form_data_models import UserDataModel

class UserData(BasePage):
    def __init__(self):
        super().__init__(template_name= "index.html", form_class=UserForm, form_model=UserDataModel, next_page="education")

    def process_form(self, form, is_multiple):
        form_data = SessionHandler.get_form_data(form)
        SessionHandler.update_session("user_data", form_data, is_multiple)
