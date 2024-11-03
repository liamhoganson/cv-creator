from ..base_page import BasePage
from ..site.forms import ProjectForm
from ..data_models.flask_form_data_models import ProjectDataModel
from ..site.session_handler import SessionHandler
from flask import session

class ProjectData(BasePage):
    def __init__(self):
        super().__init__(template_name="projects.html", form_class=ProjectForm, form_model=ProjectDataModel, next_page="skills")

    def process_form(self, form, is_multiple):
        form_data = SessionHandler.get_form_data(form)
        SessionHandler.update_session("projects_data", form_data, is_multiple)
        print(session)
