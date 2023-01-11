import os
from flask import Blueprint
from flask_restx import Api
from app.resources.bee import Bee, Bees
from app.resources.beekeeper import BeeKeeperRegister
from app import create_app



app = create_app()
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Bees, '/bees')
api.add_resource(Bee,  '/bees/<int:bee_id>')

#api.add_resource(BeeKeeperRegister, '/register/')
#api.add_resource(Bee,  '/beekeepers/meliponaries')

app.register_blueprint(api_bp, url_prefix="/v1") 

if __name__ == '__main__':
    app.run()
