from flask import Blueprint
from flask_restx import Api

from app.models.beekeeper_model import BeeKeeperModel
from app.resources.bee import Bee, Bees
from app.resources.beehive import BeeHives, BeeHive
from app.resources.beekeeper import ( BeeKeeper,
                                      BeeKeeperLogin, 
                                      BeeKeeperLogout )
from app.blocklist import BLOCKLIST
from app import create_app
from app.resources.meliponary import ( Meliponary,
                                       Meliponaries )

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

#Meliponary Resources
api.add_resource(Meliponaries, '/meliponaries')
api.add_resource(Meliponary,   '/meliponaries/<int:meliponary_id>')

api.add_resource(BeeHives, '/beehives')
api.add_resource(BeeHive, '/beehives/<int:hive_id>')





if __name__ == '__main__':
    app.run()
