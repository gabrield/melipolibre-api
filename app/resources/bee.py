import json
from flask_restful import Resource, reqparse
from app.models.bee_model import BeeModel

class Bees(Resource):
        params = reqparse.RequestParser()
        params.add_argument('genus', type=str)
        params.add_argument('subgenus', type=str)
        params.add_argument('specie', type=str)
        params.add_argument('common_name', type=str)

        @staticmethod
        def normalize(val: str):
            return '%'+val+'%'
        
        def get(self):
            params = Bees.params.parse_args()
            
            #filter only path params which are not None
            valid_params = {key:params[key] for key in params if params[key] is not None}

            #return all bees if no parameter is passed
            if (len(valid_params) == 0):
                return {'bees': [bee.json() for bee in BeeModel.query.all()]}

            query = BeeModel.query
 
            if valid_params.get('genus'):
                query = query.filter(BeeModel.genus.like(self.normalize(valid_params["genus"])))
            if valid_params.get('subgenus'):
                query = query.filter(BeeModel.subgenus.like(self.normalize(valid_params["subgenus"])))
            if valid_params.get('specie'):
                query = query.filter(BeeModel.specie.like(self.normalize(valid_params["specie"])))
            if valid_params.get('common_name'):
                query = query.filter(BeeModel.common_name.like(self.normalize(valid_params["common_name"])))
 
            return {"bees": [bee.json() for bee in query]}
