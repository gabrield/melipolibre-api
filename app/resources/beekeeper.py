import json
import bcrypt
from instance.config import Config
from flask_restx import Resource, reqparse, inputs
from flask_jwt_extended import (create_access_token, jwt_required,
                                get_jwt, get_jwt_identity,
                                current_user)

from app.database import db
from app.blueprint_api import blueprint, api
from app.blocklist import jwt_redis_blocklist
from app.models.beekeeper_model import BeeKeeperModel


def password_type(password):
    if not isinstance(password, str):
        raise ValueError('This is not password_type')
    if len(password) < 8:
        raise ValueError('Password must  contain at least 8 characters')
    return password


params = reqparse.RequestParser()
params.add_argument('name', type=str)
params.add_argument('email', type=inputs.email(),
                    required=True,
                    help="An valid email address required!",
                    trim=True)
params.add_argument('password', type=password_type,
                    required=True,
                    help="A valid password required!",
                    trim=True)


class BeeKeeper(Resource):
    @api.doc(params={'email': 'User\'s email'})
    @api.doc(params={'name': 'User\'s name'})
    @api.doc(params={'password': 'A password greater than 8 characters'})
    def post(self):
        _params = params.parse_args()
        beekeeper = BeeKeeperModel.query.filter(
            BeeKeeperModel.email == _params['email']).first()
        if beekeeper:
            return {'message': 'user already registered'}, 409

        beekeeper = BeeKeeperModel(**_params)
        db.session.add(beekeeper)
        db.session.commit()

        return {'message': f'{beekeeper.email} created.... Check your email for activation'}, 201

    @jwt_required()
    def delete(self):
        BeeKeeperModel.query.filter_by(id=current_user.id).delete()
        db.session.commit()
        jwt = get_jwt()  # JWT Token Identifier
        BeeKeeperLogout.logout(jwt)
        return {'message': 'User deleted sucessfully!'}, 200

    @jwt_required()
    def put(self):
        _params = params.parse_args()
        BeeKeeperModel.query.filter_by(id=current_user.id).update(_params)
        db.session.commit()
        # logout after update
        jwt = get_jwt()
        BeeKeeperLogout.logout(jwt)
        return {'message': 'user updated'}, 200


class BeeKeeperLogin(Resource):
    def post(self):
        _params = params.parse_args()

        beekeeper = BeeKeeperModel.query.filter(
            BeeKeeperModel.email == _params['email']).first()
        if beekeeper:
            if beekeeper.password == _params['password']:
                access_token = create_access_token(identity=beekeeper.id)
                return {'access_token': access_token}, 200

        return {'message': 'Wrong user or password'}, 401


class BeeKeeperLogout(Resource):
    @classmethod
    def logout(cls, jwt):
        jwt_redis_blocklist.set(
            jwt['jti'], "", ex=Config.JWT_ACCESS_TOKEN_EXPIRES)

    @jwt_required()
    def post(self):
        jwt = get_jwt()
        BeeKeeperLogout.logout(jwt)
        return {'message': 'Logged out successfully!'}, 200
