from ..base_page import BasePage
from ..site.forms import ExperienceForm
from ..site.session_handler import SessionHandler
from ..data_models.flask_form_data_models import ExperienceDataModel

class ExperienceData(BasePage):
    def __init__(self):
        super().__init__(template_name="experience.html", form_class=ExperienceForm, form_name="experience_form", form_model=ExperienceDataModel, next_page="projects")

    def process_form(self, form, is_multiple):
        form_data = SessionHandler.get_form_data(form)
        SessionHandler.update_session("experience_data", form_data, is_multiple)