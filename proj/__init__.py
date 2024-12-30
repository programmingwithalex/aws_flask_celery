''' Application Factory Pattern '''
import os

from flask import Flask

from . import extensions
from .config import config


def create_app(config_name: str = None) -> Flask:
    ''' load configuration and create Flask app '''
    if not config_name:
        config_name = os.environ.get('FLASK_CONFIG', 'development')

    # uncomment to print config
    # print(f'config_name: {config_name}')

    # instantiate the app
    app = Flask(__name__)

    # set config
    app.config.from_object(config[config_name])

    # set up extensions
    extensions.mail.init_app(app)

    return app
