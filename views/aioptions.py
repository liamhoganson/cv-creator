from ..base_page import BasePage
from ..site.forms import AiOptionsForm
from ..data_models.flask_form_data_models import AiOptionsModel
from ..site.session_handler import SessionHandler

class AiOptionsData(BasePage):
    def __init__(self):
        super().__init__(template_name="aioptions.html", form_class=AiOptionsForm, form_name="aioptions_form", form_model=AiOptionsModel, next_page="submit")

    def process_form(self, form, is_multiple):
        form_data = SessionHandler.get_form_data(form)
        SessionHandler.update_session("aioptions_data", form_data, is_multiple)
