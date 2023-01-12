import json
from flask_restx import Resource, reqparse
from app.models.bee_model import BeeModel
from app import filters


class Bees(Resource):
        params = reqparse.RequestParser()
        params.add_argument('genus', type=str)
        params.add_argument('subgenus', type=str)
        params.add_argument('specie', type=str)
        params.add_argument('common_name', type=str)

        def get(self):
            params = Bees.params.parse_args()
            
            #filter only valid params which are not None
            valid_params = filters.valid_req_params(params)

            #return all bees if no parameter is passed
            if len(valid_params) == 0:
                return {'bees': [bee.json() for bee in BeeModel.query.all()]}

            query = BeeModel.query
 
            if valid_params.get('genus'):
                query = query.filter(BeeModel.genus.contains(valid_params["genus"]))
            if valid_params.get('subgenus'):
                query = query.filter(BeeModel.subgenus.contains(valid_params["subgenus"]))
            if valid_params.get('specie'):
                query = query.filter(BeeModel.specie.contains(valid_params["specie"]))
            if valid_params.get('common_name'):
                query = query.filter(BeeModel.common_name.contains(valid_params["common_name"]))
 
            return {"bees": [bee.json() for bee in query]}


class Bee(Resource):
    def get(self, bee_id):
        try:
            return BeeModel.query.get(bee_id).json()
        except:
            return {'message' : 'bee not found'}, 404


        