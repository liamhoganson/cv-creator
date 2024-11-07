from ..base_page import BasePage
from ..app_site.forms import ProjectForm
from ..data_models.flask_form_data_models import ProjectDataModel
from ..app_site.session_handler import SessionHandler

class ProjectData(BasePage):
    def __init__(self):
        super().__init__(template_name="projects.html", form_class=ProjectForm, form_model=ProjectDataModel, next_page="skills")

    def process_form(self, form, is_multiple):
        form_data = SessionHandler.get_form_data(form)
        SessionHandler.update_session("projects_data", form_data, is_multiple)
