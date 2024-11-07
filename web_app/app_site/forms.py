from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, BooleanField, URLField, TextAreaField, FieldList, FormField, SubmitField, DateField, SelectField
from wtforms.validators import InputRequired, Email, URL, Optional

class EducationForm(FlaskForm):
    university = StringField("University", validators=[Optional()])
    location = StringField("University Location", validators=[Optional()])
    degree = StringField("Degree", validators=[Optional()])
    university_start_date = DateField("University Start Date", format='%Y-%m-%d', validators=[Optional()])
    university_end_date = DateField("University End Date (Leave blank if present)", format='%Y-%m-%d', validators=[Optional()])
    add_another = SelectField("Add another Education entry?", choices=[("no", "No"), ("yes", "Yes")], default="no")
    submit = SubmitField("Next")

class ExperienceForm(FlaskForm):
    title = StringField("Job Title", validators=[Optional()])
    company = StringField("Company Name", validators=[Optional()])
    location = StringField("Job Location", validators=[Optional()])
    job_start_date = DateField("Job Start Date", format='%Y-%m-%d', validators=[Optional()])
    job_end_date = DateField("Job End Date (Leave blank if present)", format='%Y-%m-%d', validators=[Optional()])
    job_functions = TextAreaField("Job Functions", validators=[Optional()])
    add_another = SelectField("Add another Job?", choices=[("no", "No"), ("yes", "Yes")], default="no")
    submit = SubmitField("Next")

class ProjectForm(FlaskForm):
    project_name = StringField("Project Name", validators=[Optional()])
    github_repo_link = URLField("GitHub Project Link", validators=[Optional()])
    skills_learned = TextAreaField("Skills Learned", validators=[Optional()])
    project_functions = TextAreaField("Project Functions", validators=[Optional()])
    add_another = SelectField("Add another Project?", choices=[("no", "No"), ("yes", "Yes")], default="no")
    submit = SubmitField("Next")

class SkillsForm(FlaskForm):
    skills_list = TextAreaField("List of Skills", validators=[Optional()])
    submit = SubmitField("Next")

class CertsForm(FlaskForm):
    certs_list = TextAreaField("List of Certifications", validators=[Optional()])
    submit = SubmitField("Next")

class AiOptionsForm(FlaskForm):
    add_summary = SelectField("Do you want an AI generated summary?", choices=[("no", "No"), ("yes", "Yes")], default="no")
    edit_attributes = SelectField("Do you want AI to enhance your resume?", choices=[("no", "No"), ("yes", "Yes")], default="no")
    job_desc = TextAreaField("(Optional) Paste Job Description:", validators=[Optional()])

class UserForm(FlaskForm):
    full_name = StringField("Full Name", validators=[InputRequired()])
    phone_number = StringField("Phone Number", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    linkedin = URLField("LinkedIn Profile URL", validators=[URL(), Optional()])
    github = URLField("Github Profile URL", validators=[URL(), Optional()])
    submit = SubmitField("Next")
