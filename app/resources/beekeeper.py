import json, hmac, bcrypt
from flask_restx import Resource, reqparse, inputs
from flask_jwt_extended import (create_access_token, jwt_required,
                                        get_jwt, get_jwt_identity,
                                                    current_user)

from app.database import db
from app.blocklist import BLOCKLIST
from app.models.beekeeper_model import BeeKeeperModel

params = reqparse.RequestParser()
params.add_argument('name', type=str)
params.add_argument('email', type=inputs.email(), required=True, \
    help="An valid email address required!", trim=True)
params.add_argument('password', type=str, required=True, help="Password required!", \
            trim=True)

class BeKeeper(Resource):
    def post(self):
        _params = params.parse_args()
        beekeeper = BeeKeeperModel.query.filter(BeeKeeperModel.email == _params['email']).first()
        if beekeeper:
            return {'message': 'user already registered'}, 409
        #encrypt password
        
        beekeeper = BeeKeeperModel(**_params)
        byte_password = beekeeper.password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(byte_password, salt)
        beekeeper.password = password_hash
        db.session.add(beekeeper)
        db.session.commit()
        
        return {'message' : f'{beekeeper.email} created.... Check your email for activation'}, 201
    
    @jwt_required()
    def delete(self):
        BeeKeeperModel.query.filter_by(id=current_user.id).delete()
        db.session.commit()
        jwt = get_jwt() #JWT Token Identifier
        BeeKeeperLogout.logout(jwt)
        return {'message':'User deleted sucessfully!'}, 200\

    @jwt_required()
    def put(self):
        _params = params.parse_args()
        BeeKeeperModel.query.filter_by(id=current_user.id).update(_params)
        db.session.commit()
        #logout after update
        jwt = get_jwt()
        BeeKeeperLogout.logout(jwt)
        return {'message' : 'user updated'}, 200
            


class BeeKeeperLogin(Resource):
    def post(self):
        _params = params.parse_args()
        beekeeper = BeeKeeperModel.query.filter(BeeKeeperModel.email == _params['email']).firs
        if beekeeper and bcrypt.checkpw(_params['password'].encode('utf-8'), beekeeper.password):
            access_token = create_access_token(identity=beekeeper.id)
            return {'access_token' : access_token}, 200
        
        return {'message': 'Wrong user or password'}, 401


class BeeKeeperLogout(Resource):
    @classmethod
    def logout(cls, jwt):
        BLOCKLIST.add(jwt['jti'])
        
    @jwt_required()
    def post(self):
        jwt = get_jwt()
        BeeKeeperLogout.logout(jwt)
        return {'message' : 'Logged out successfully!'}, 200
   