from flask import request, redirect, url_for, render_template
from .abc import AbstractPage
import json

#TODO: Add custom error for pydantic validation errors

class BasePage(AbstractPage):
    '''
    Base page class used to construct subclass views
    '''
    def __init__(self, template_name: str, form_class: object, form_name: str, form_model: object, next_page: str): ##TODO: Dynamically get form name from form class
        self.template_name = template_name
        self.form_class = form_class
        self.form_name = form_name     # str(form_class.__name__).lower()
        self.form_model = form_model
        self.current_page = f"site.{form_name.split('_')[0]}" ## form names must adhere to functionname_form naming convention
        self.next_page = "site."+next_page

    def form_validator(self, **kwargs) -> dict:
        '''
        Uses form's pydantic model to validate form data
        '''
        try:
            validator = self.form_model(**request.form)
            return json.loads(validator.json())
        except ValueError as e:
            print(e)
            return render_template("400.html")

    # GET/POST backend function
    def handle_request(self) -> object:
        '''
        Handles incoming HTTP requests, validates and redirects as needed.
        '''
        form_instance = self.form_class()
        if request.method == "POST" and form_instance.validate_on_submit():

            validation_result = self.form_validator()
            if request.form.get('add_another'):
                self.process_form(validation_result, is_multiple = True)

                if request.form.get("add_another") == 'yes':
                    return redirect(url_for(self.current_page))
            else:
                self.process_form(validation_result, is_multiple = False)
            return redirect(url_for(self.next_page))

        return render_template(self.template_name, **{self.form_name: form_instance})
