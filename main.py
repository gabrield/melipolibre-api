import json
import os
from flask import Flask, Blueprint
from flask_restful import Api
from app.resources.bee import Bees
from app.models.bee import BeeModel
from app.database import db
from app import create_app


config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
api_bp = Blueprint('bees', __name__)
api = Api(api_bp)

@app.before_first_request
def create_database():
    db.drop_all()
    db.create_all()
    with open('asf_list.json') as bee_file:
        bees =  json.load(bee_file)
        db.session.bulk_save_objects([BeeModel(**bee) for bee in bees])
        db.session.commit()
    

#bee resources
api.add_resource(Bees, '/bees')
app.register_blueprint(api_bp)
#api.add_resource(Bee, '/bee')


if __name__ == '__main__':
    app.run()
