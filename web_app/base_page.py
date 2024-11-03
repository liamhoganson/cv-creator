import json
from flask import request, redirect, url_for, render_template
from .abc import AbstractPage

class BasePage(AbstractPage):
    '''
    Base page class used to construct subclass views
    '''
    def __init__(self, template_name: str, form_class: object, form_model: object, next_page: str): ##TODO: Refactor some of these params
        self.template_name = template_name
        self.form_class = form_class
        self.form_name = str(form_class.__name__).replace('Form', '_form').lower()
        self.form_model = form_model
        self.current_page = f"site.{self.form_name.split('_')[0]}" ## form names must adhere to functionname_form naming convention
        self.next_page = "site."+next_page

    def form_validator(self, **kwargs) -> dict:
        '''
        Uses form's pydantic model to validate form data
        '''
        try:
            validator = self.form_model(**request.form)
            return json.loads(validator.json())
        except Exception:
            return None

    # GET/POST backend function
    def handle_request(self) -> object:
        '''
        Handles incoming HTTP requests, validates and redirects as needed.
        '''
        form_instance = self.form_class()
        if request.method == "POST" and form_instance.validate_on_submit():

            validation_result = self.form_validator()
            if validation_result is None:
                return render_template("500.html")
            if request.form.get('add_another'):
                self.process_form(validation_result, is_multiple = True)

                if request.form.get("add_another") == 'yes':
                    return redirect(url_for(self.current_page))
            else:
                self.process_form(validation_result, is_multiple = False)
            return redirect(url_for(self.next_page))

        return render_template(self.template_name, **{self.form_name: form_instance})
