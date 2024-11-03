from ..base_page import BasePage
from ..site.forms import SkillsForm
from ..data_models.flask_form_data_models import SkillsDataModel
from ..site.session_handler import SessionHandler

class SkillsData(BasePage):
    def __init__(self):
        super().__init__(template_name="skills.html", form_class=SkillsForm, form_model=SkillsDataModel, next_page="certs")

    def process_form(self, form, is_multiple):
        form_data = SessionHandler.get_form_data(form)
        SessionHandler.update_session("skills_data", form_data, is_multiple)
