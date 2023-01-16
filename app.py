from flask import Blueprint
from flask_restx import Api

from app.models.beekeeper_model import BeeKeeperModel
from app.resources.bee import Bee, Bees
from app.resources.beekeeper import BeeKeeper, \
    BeeKeeperLogin, BeeKeeperLogout
from app.blocklist import BLOCKLIST
from app import create_app

app = create_app()

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
app.register_blueprint(api_bp, url_prefix="/v1")




#Bee Resources
api.add_resource(Bees, '/bees')
api.add_resource(Bee,  '/bees/<int:bee_id>')

#BeeKeeper Resources
api.add_resource(BeeKeeper, '/beekeepers/') # POST / PUT / DELETE methods  
api.add_resource(BeeKeeperLogin, '/login')
api.add_resource(BeeKeeperLogout, '/logout')

if __name__ == '__main__':
    app.run()
