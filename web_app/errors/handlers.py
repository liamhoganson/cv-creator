from flask import render_template, Blueprint

# Blueprint Constructor
errors = Blueprint('errors', __name__)

@errors.app_errorhandler(400)
def not_found_error(error):
    return render_template('400.html'), 400

@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@errors.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# @errors.app_errorhandler(304)
# def validation_error(error):
#     return render_template('400.html') #TODO: Update to right error template