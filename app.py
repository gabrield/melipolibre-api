from flask import jsonify, Blueprint
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.models.beekeeper_model import BeeKeeperModel
from app.resources.bee import Bee, Bees
from app.resources.beekeeper import BeeKeeper, \
    BeeKeeperLogin, BeeKeeperLogout
from app.blocklist import BLOCKLIST
from app import create_app

app = create_app()
jwt = JWTManager(app)
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




@jwt.token_in_blocklist_loader
def token_in_blocklist(jwt_header, jwt_payload: dict):
    return jwt_payload['jti'] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token(jwt_header, jwt_payload: dict):
    return jsonify({'message' : 'invalid token / logged out'}), 401


@jwt.user_identity_loader
def user_identity_lookup(beekeeper):
    return beekeeper


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup(_jwt_header, jwt_payload: dict):
    identity = jwt_payload["sub"]
    return BeeKeeperModel.query.filter_by(id=identity).one_or_none()

if __name__ == '__main__':
    app.run()
