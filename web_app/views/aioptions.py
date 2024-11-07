import asyncio
from ..base_page import BasePage
from ..app_site.forms import AiOptionsForm
from ..data_models.flask_form_data_models import AiOptionsModel
from ..app_site.session_handler import SessionHandler
from ..app_site.payload_factory import PayloadFactory

class AiOptionsData(BasePage):
    def __init__(self):
        super().__init__(template_name="aioptions.html", form_class=AiOptionsForm, form_model=AiOptionsModel, next_page="submit")

    def process_form(self, form, is_multiple):
        form_data = SessionHandler.get_form_data(form)
        SessionHandler.update_session("ai_options_data", form_data, is_multiple)
        print(asyncio.run(PayloadFactory().convert_session_to_payload()))