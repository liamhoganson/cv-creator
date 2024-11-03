from flask import Flask
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
from flask_session import Session
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem' ##TODO: Implement Redis
    Session(app)

    csrf = CSRFProtect(app)

    from .site.routes import site
    from .errors.handlers import errors

    app.register_blueprint(site)
    app.register_blueprint(errors)

    return app
