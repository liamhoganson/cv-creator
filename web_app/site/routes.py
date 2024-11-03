# Imports
from flask import Blueprint, render_template
from .forms import *

from ..views.user_info import UserData
from ..views.education import EducationData
from ..views.experience import ExperienceData
from ..views.projects import ProjectData
from ..views.skills import SkillsData
from ..views.certs import CertsData
from ..views.aioptions import AiOptionsData

# Blueprint constructor
site = Blueprint("site", __name__)

# Main Entry / User Data Form
@site.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    page = UserData()
    return page.handle_request()

@site.route('/education', methods=['GET', 'POST'])
def education():
    page = EducationData()
    return page.handle_request()

@site.route('/experience', methods=['GET', 'POST'])
def experience():
    page = ExperienceData()
    return page.handle_request()

@site.route('/projects', methods=['GET', 'POST'])
def projects():
    page = ProjectData()
    return page.handle_request()

@site.route('/skills', methods=['GET', 'POST'])
def skills():
    page = SkillsData()
    return page.handle_request()

@site.route('/certs', methods=['GET', 'POST'])
def certs():
    page = CertsData()
    return page.handle_request()

@site.route('/aioptions', methods=['GET', 'POST'])
def aioptions():
    page = AiOptionsData()
    return page.handle_request()

@site.route("/submit", methods=["GET"])
def submit():
    return render_template("submitted.html")
