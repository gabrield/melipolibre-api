# melipolibre-api/__init__.py
import os, json
from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
# local import
from instance.config import app_config
from app.models.bee_model import BeeModel
from app.resources.bee import Bees
from app.blocklist import BLOCKLIST


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_name = os.getenv('APP_SETTINGS')
    app.config.from_object(app_config[config_name] or app_config['development'])
    from app.database import db
    db.init_app(app)
    
    @app.before_first_request
    def create_database():
        db.drop_all()
        db.create_all()
        with open(os.path.dirname(os.path.abspath(__file__)) + \
            '/data/asf_list.json', encoding='utf-8') as bee_file:
            bees =  json.load(bee_file)
            db.session.bulk_save_objects([BeeModel(**bee) for bee in bees])
            db.session.commit()

    return app
