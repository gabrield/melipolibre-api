import json, hmac
from flask_restx import Resource, reqparse, inputs
from flask_jwt_extended import create_access_token, jwt_required, \
                               get_jwt, get_jwt_identity
from app import filters
from app.blocklist import BLOCKLIST
from app.database import db
from app.models.beekeeper_model import BeeKeeperModel



params = reqparse.RequestParser()
params.add_argument('name', type=str)
params.add_argument('email', type=inputs.email(), required=True, \
    help="An valid email address required!", trim=True)
params.add_argument('password', type=str, required=True, help="Password required!", \
            trim=True)

class BeeKeeper(Resource):
        def post(self):
            _params = params.parse_args()
            valid_params = filters.valid_req_params(_params)
            beekeeper = BeeKeeperModel.query.filter(BeeKeeperModel.email == valid_params['email']).first()

            if beekeeper:
                return {'message': 'user already registered'}, 409
            
            beekeeper = BeeKeeperModel(**valid_params)
            db.session.add(beekeeper)
            db.session.commit()
            
            return {'message' : f'{beekeeper.email} created.... Check your email for activation'}, 201
        
        @jwt_required()
        def delete(self):
            beekeeper_id = get_jwt_identity()
            BeeKeeperModel.query.filter_by(id=beekeeper_id).delete()
            db.session.commit()

            jwt = get_jwt()['jti'] #JWT Token Identifier
            BLOCKLIST.add(jwt)

            return {'message':'User deleted sucessfully!'}, 200

        @jwt_required()
        def put(self):
            _params = params.parse_args()
            valid_params = filters.valid_req_params(_params)
            beekeeper_id = get_jwt_identity()
            BeeKeeperModel.query.filter_by(id=beekeeper_id).update(valid_params)
            db.session.commit()

            return {'message' : 'user updated'}, 200

            


class BeeKeeperLogin(Resource):
        def post(self):
            _params = params.parse_args()
            valid_params = filters.valid_req_params(_params)
            beekeeper = BeeKeeperModel.query.filter(BeeKeeperModel.email == valid_params['email']).first()

            if beekeeper and hmac.compare_digest(beekeeper.password, valid_params['password']):
                access_token = create_access_token(identity=beekeeper.id)
                return {'access_token' : access_token}
            
            return {'message': 'Wrong user or password'}, 401


class BeeKeeperLogout(Resource):
        @jwt_required()
        def post(self):
            jwt = get_jwt()['jti'] #JWT Token Identifier
            BLOCKLIST.add(jwt)
            return {'message' : 'Logged out successfully!'}, 200