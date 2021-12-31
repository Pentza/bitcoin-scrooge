from flask import Flask
from .main import main as main_blueprint
from .config import SECRET

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET

    app.register_blueprint(main_blueprint)

    return app
