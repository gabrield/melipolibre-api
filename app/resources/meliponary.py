import json, hmac
from flask_restx import Resource, reqparse, inputs
from flask_jwt_extended import (create_access_token, 
                                       jwt_required,
                                            get_jwt, 
                                   get_jwt_identity,
                                       current_user)
from app import filters
from app.blocklist import BLOCKLIST
from app.database import db
from app.models.meliponary_model import MeliponaryModel

params = reqparse.RequestParser()
params.add_argument('name', type=str, required=True, trim=True)
params.add_argument('address', type=str, required=True, trim=True)

class Meliponaries(Resource):
        @jwt_required()
        def get(self):
            return {'meliponaries': [meliponary.json() \
                for meliponary in current_user.meliponaries]
            }

    
        @jwt_required()
        def post(self):
            _params = params.parse_args()
            valid_params = filters.valid_req_params(_params)
            meliponary = MeliponaryModel(**valid_params, beekeeper=current_user)
            db.session.add(meliponary)
            db.session.commit()
            return {'message' : f'{meliponary.name} created!'}, 201


class Meliponary(Resource):
        @jwt_required()
        def get(self, meliponary_id):
            return MeliponaryModel.query.get(meliponary_id)