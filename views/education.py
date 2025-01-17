from ..base_page import BasePage
from ..site.forms import EducationForm
from ..site.session_handler import SessionHandler
from ..data_models.flask_form_data_models import EducationDataModel

class EducationData(BasePage):
    def __init__(self):
        super().__init__(template_name="education.html", form_class=EducationForm, form_name="education_form", form_model=EducationDataModel, next_page="experience")

    def process_form(self, form, is_multiple):
        form_data = SessionHandler.get_form_data(form)
        print(form_data)
        print(SessionHandler.update_session("education_data", form_data, is_multiple))
