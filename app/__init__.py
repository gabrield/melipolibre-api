# melipolibre-api/__init__.py
import os
import json
from app.blocklist import jwt_redis_blocklist
from app.database import db
from app.blueprint_api import blueprint, api
# from app.api import api
from instance.config import app_config
from flask import Flask, jsonify, url_for
from flask_restx import Api
# JWT
from flask_jwt_extended import JWTManager
# Models
from app.models.bee_model import BeeModel
from app.models.beekeeper_model import BeeKeeperModel
# resources
from app.resources.bee import Bee, Bees
from app.resources.beehive import BeeHives, BeeHive
from app.resources.beekeeper import (BeeKeeper,
                                     BeeKeeperLogin,
                                     BeeKeeperLogout)
from app.resources.meliponary import (Meliponary,
                                      Meliponaries)


from app.resources.handling import Handlings


def load_bees():
    db.drop_all()
    db.create_all()
    with open(os.path.dirname(os.path.abspath(__file__)) +
              '/data/asf_list.json', encoding='utf-8') as bee_file:
        bees = json.load(bee_file)
        db.session.bulk_save_objects([BeeModel(**bee) for bee in bees])
        db.session.commit()


def register_resources(api: Api):
    # Bee Resources
    api.add_resource(Bees, '/bees')
    api.add_resource(Bee,  '/bees/<int:bee_id>')

    # BeeKeeper Resources
    api.add_resource(BeeKeeper, '/beekeepers')  # POST / PUT / DELETE methods
    api.add_resource(BeeKeeperLogin, '/login')
    api.add_resource(BeeKeeperLogout, '/logout')

    # Meliponary Resources
    api.add_resource(Meliponaries, '/meliponaries')
    api.add_resource(Meliponary,   '/meliponaries/<int:meliponary_id>')

    # Beehive Resources
    api.add_resource(BeeHives, '/beehives')
    api.add_resource(BeeHive, '/beehives/<int:hive_id>')

    # Handlings Resources
    api.add_resource(Handlings, '/handlings')
    # api.add_resource(BeeHive, '/beehives/<int:hive_id>')


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_name = os.getenv('APP_SETTINGS') or 'development'
    app.config.from_object(app_config[config_name])

    db.init_app(app)
    jwt = JWTManager(app)
    # blueprint = Blueprint('melipolibre-api', __name__)
    # api = Api(blueprint)
    app.register_blueprint(blueprint, url_prefix="/v1")

    # Setup our redis connection for storing the blocklisted tokens. You will probably
    # want your redis instance configured to persist data to disk, so that a restart
    # does not cause your application to forget that a JWT was revoked.

    with app.app_context():
        register_resources(api)
        load_bees()

    @jwt.token_in_blocklist_loader
    def token_in_blocklist(jwt_header, jwt_payload: dict):
        try:
            jti = jwt_payload["jti"]
            token_in_redis = jwt_redis_blocklist.get(jti)
            return token_in_redis is not None
        except:
            return False

    @jwt.revoked_token_loader
    def revoked_token(jwt_header, jwt_payload: dict):
        return jsonify({'message': 'revoked token / logged out'}), 401

    @jwt.token_verification_loader
    def token_verification_failed(jwt_header, jwt_payload: dict):
        return jsonify({'message': 'token_verification_failed'}), 401

    @jwt.invalid_token_loader
    def invalid_token(invalid_token_message: str):
        return jsonify({'message': f'invalid token:\n{invalid_token_message}'}), 401

    @jwt.user_identity_loader
    def user_identity(beekeeper):
        return beekeeper

    # Register a callback function that loads a user from your database whenever
    # a protected route is accessed. This should return any python object on a
    # successful lookup, or None if the lookup failed for any reason (for example
    # if the user has been deleted from the database).

    @jwt.user_lookup_loader
    def user_lookup(_jwt_header, jwt_payload: dict):
        identity = jwt_payload["sub"]
        return BeeKeeperModel.query.filter_by(id=identity).one_or_none()

    return app
