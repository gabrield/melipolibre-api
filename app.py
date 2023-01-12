from flask import json, Blueprint
from flask_restx import Api
from app.resources.bee import Bee, Bees
from app.resources.beekeeper import BeeKeeperRegister
from app import create_app

app = create_app()
api_bp = Blueprint('melipolibre-api', __name__)
api = Api(api_bp, version='0.1', title='Melipolibre API',
    description='A simple API for beekeeping apps',)

#Bee Resources
api.add_resource(Bees, '/bees')
api.add_resource(Bee,  '/bees/<int:bee_id>')

api.add_resource(BeeKeeperRegister, '/register')
#api.add_resource(Bee,  '/beekeepers/meliponaries')
app.register_blueprint(api_bp, url_prefix="/v1")



#with app.app_context():
#    urlvars = False  # Build query strings in URLs
#    swagger = True  # Export Swagger specifications
#    data = api.as_postman(urlvars=urlvars, swagger=swagger)
#    print(json.dumps(data))


if __name__ == '__main__':
    app.run()
