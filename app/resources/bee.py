import json
from flask_restful import Resource, reqparse
from app.models.bee_model import BeeModel


class Bees(Resource):
        params = reqparse.RequestParser()
        params.add_argument('genus', type=str)
        params.add_argument('subgenus', type=str)
        params.add_argument('specie', type=str)
        params.add_argument('common_name', type=str)

        def get(self):
            params = Bees.params.parse_args()
            
            #filter only path params which are not None
            valid_params = {key:params[key] for key in params if params[key] is not None}

            #return all bees if no parameter is passed
            if len(valid_params) == 0:
                return {'bees': [bee.json() for bee in Bee.query.all()]}

            query = Bee.query
 
            if valid_params.get('genus'):
                query = query.filter(Bee.genus.contains(valid_params["genus"]))
            if valid_params.get('subgenus'):
                query = query.filter(Bee.subgenus.contains(valid_params["subgenus"]))
            if valid_params.get('specie'):
                query = query.filter(Bee.specie.contains(valid_params["specie"]))
            if valid_params.get('common_name'):
                query = query.filter(Bee.common_name.contains(valid_params["common_name"]))
 
            return {"bees": [bee.json() for bee in query]}
