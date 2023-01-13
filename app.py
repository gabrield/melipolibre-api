from flask import jsonify, Blueprint
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.resources.bee import Bee, Bees
from app.resources.beekeeper import BeeKeeper, \
    BeeKeeperLogin, BeeKeeperLogout
from app.blocklist import BLOCKLIST
from app import create_app

app = create_app()
jwt = JWTManager(app)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)



#Bee Resources
api.add_resource(Bees, '/bees')
api.add_resource(Bee,  '/bees/<int:bee_id>')

#BeeKeeper Resources
api.add_resource(BeeKeeper, '/beekeepers/') # POST / PUT / DELETE methods  
api.add_resource(BeeKeeperLogin, '/login')
api.add_resource(BeeKeeperLogout, '/logout')

@jwt.token_in_blocklist_loader
def check_blocklist(jwt_header, jwt_payload: dict):
    return jwt_payload['jti'] in BLOCKLIST

@jwt.revoked_token_loader
def invalidated_access_token(jwt_header, jwt_payload: dict):
    return jsonify({'message' : 'invalid token / logged out'}), 401

if __name__ == '__main__':
    app.register_blueprint(api_bp, url_prefix="/v1")
    app.run()
