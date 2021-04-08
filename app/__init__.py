# nativasf/__init__.py

from flask import Flask
# local import
from instance.config import app_config



def create_app(config_name):
    print("CONFIG NAME:", config_name)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    from .database import db
    db.init_app(app)

    return app
