# melipolibre-api/__init__.py
import os
from flask import Flask
# local import
from instance.config import app_config
from app.models.bee_model import Bee
from app.resources.bee import Bees
import json



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
            '/data/asf_list.json') as bee_file:
            bees =  json.load(bee_file)
            db.session.bulk_save_objects([Bee(**bee) for bee in bees])
            db.session.commit()

    return app
