# melipolibre-api/__init__.py
import os, json
from flask import Flask, Blueprint, jsonify
from flask_jwt_extended import JWTManager
# local import
from instance.config import app_config
from app.models.bee_model import BeeModel
from app.models.beekeeper_model import BeeKeeperModel
from app.blocklist import BLOCKLIST


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_name = os.getenv('APP_SETTINGS') or 'development'
    app.config.from_object(app_config[config_name])
    from app.database import db
    db.init_app(app)
    jwt = JWTManager(app)

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
