from ..base_page import BasePage
from ..site.forms import CertsForm
from ..data_models.flask_form_data_models import CertsDataModel
from ..site.session_handler import SessionHandler

class CertsData(BasePage):
    def __init__(self):
        super().__init__(template_name="certs.html", form_class=CertsForm, form_name="certs_form", form_model=CertsDataModel, next_page="aioptions")

    def process_form(self, form, is_multiple):
        form_data = SessionHandler.get_form_data(form)
        SessionHandler.update_session("certs_data", form_data, is_multiple)
