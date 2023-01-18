import json
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required
from app.models.bee_model import BeeModel

class Bees(Resource):
        params = reqparse.RequestParser()
        params.add_argument('genus', type=str)
        params.add_argument('subgenus', type=str)
        params.add_argument('specie', type=str)
        params.add_argument('common_name', type=str)

        @jwt_required()
        def get(self):
            _params = Bees.params.parse_args()
            #return all bees if no parameter is passed
            if len(_params) == 0:
                return {'bees': [bee.json() for bee in BeeModel.query.all()]}, 200

            query = BeeModel.query
 
            if _params.get('genus'):
                query = query.filter(BeeModel.genus.contains(_params["genus"]))
            if _params.get('subgenus'):
                query = query.filter(BeeModel.subgenus.contains(_params["subgenus"]))
            if _params.get('specie'):
                query = query.filter(BeeModel.specie.contains(_params["specie"]))
            if _params.get('common_name'):
                query = query.filter(BeeModel.common_name.contains(_params["common_name"]))
 
            return {"bees": [bee.json() for bee in query]}, 200

class Bee(Resource):
    @jwt_required()
    def get(self, bee_id): 
        bee = BeeModel.query.get(bee_id)
        if bee: 
            return bee.json()
        return {'message' : 'Bee not found'}, 404
      


        