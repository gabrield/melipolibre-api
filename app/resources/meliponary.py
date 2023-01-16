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
        def get(self): #TODO: filter by name and/or address
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
            meliponary = MeliponaryModel.query.get(meliponary_id)

            if meliponary:
                if meliponary.beekeeper_id != current_user.id:
                    return {'message' : f'Meliponary {meliponary_id} doesn\'t belong to user'}, 401
                return meliponary.json(), 200
            
            return {'message' : f'Meliponary {meliponary_id} doesn\'t exist'}, 400


            



            
            return {'message' : 'Meliponary {meliponary_id} doesn\'t exist or belong to user'}, 

        @jwt_required()
        def put(self, meliponary_id):
            meliponary = MeliponaryModel.query.filter_by(meliponary_id=meliponary_id, \
                                                   beekeeper_id=current_user.id)
            if meliponary:
                valid_params = params.parse_args()
                meliponary.update(**valid_params)
                db.session.commit()
                return {'message' : 'Meliponary {meliponary.name} updated'}
            
            return {'message' : 'Meliponary {meliponary_id} doesn\'t exist or belong to user'}

    
        @jwt_required()
        def delete(self, meliponary_id):
            ...