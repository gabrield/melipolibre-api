import json
from flask_restx import Resource, reqparse, inputs
from flask_jwt_extended import create_access_token
import hmac
from app.database import db
from app.models.beekeeper_model import BeeKeeperModel
from app import filters

params = reqparse.RequestParser()
params.add_argument('name', type=str)
params.add_argument('email', type=inputs.email(), required=True, \
    help="An valid email address required!", trim=True)
params.add_argument('password', type=str, required=True, help="Password required!", \
            trim=True)

class BeeKeeperRegister(Resource):
        def post(self):
            _params = params.parse_args()
            valid_params = filters.valid_req_params(_params)
            beekeeper = BeeKeeperModel.query.filter(BeeKeeperModel.email == valid_params['email']).first()

            if beekeeper:
                return {'message': 'user already registered'}, 409
            try:
                beekeeper = BeeKeeperModel(**valid_params)
                db.session.add(beekeeper)
                db.session.commit()
                return {'message' : f'{beekeeper.email} created.... Check your email for activation'}, 201
            except Exception as ex:
                return {'message' : ex}, 500



class BeeKeeperLogin(Resource):
        def post(self):
            _params = params.parse_args()
            valid_params = filters.valid_req_params(_params)
            beekeeper = BeeKeeperModel.query.filter(BeeKeeperModel.email == valid_params['email']).first()

            if beekeeper and hmac.compare_digest(beekeeper.password, valid_params['password']):
                access_token = create_access_token(identity=beekeeper.id)
                return {'access_token' : access_token}
            
            return {'message': 'Wrong user or password'}, 401
