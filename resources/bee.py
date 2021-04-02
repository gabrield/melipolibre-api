from flask_restful import Resource, reqparse
import json
from models.bee import BeeModel


class Bees(Resource):

    def get(self):
        return [bee.json() for bee in BeeModel.query.all()]

class Bee(Resource):
        params = reqparse.RequestParser()
        params.add_argument('genus', type=str)
        params.add_argument('subgenus', type=str)
        params.add_argument('specie', type=str)
        params.add_argument('common_name', type=str)
        params.add_argument('occurrence_area', type=str)

        @staticmethod
        def normalize(val: str):
            return '%'+val+'%'
        
        def get(self):
            params = Bee.params.parse_args()

            valid_params = {key:params[key] for key in params if params[key] is not None}

            if (len(valid_params) == 0):
                return [bee.json() for bee in BeeModel.query.all()]


 
            query = BeeModel.query
 
            if params["genus"]:
                query = query.filter(BeeModel.genus.like(self.normalize(params["genus"])))
            if params["subgenus"]:
                query = query.filter(BeeModel.subgenus.like(self.normalize(params["subgenus"])))
            if params["specie"]:
                query = query.filter(BeeModel.specie.like(self.normalize(params["specie"])))
            if params["common_name"]:
                query = query.filter(BeeModel.common_name.like(self.normalize(params["common_name"])))
            if params["occurrence_area"]:
                query = query.filter(BeeModel.occurrence_area.like(self.normalize(params["occurrence_area"])))
 
            return {"bees": [bee.json() for bee in query]}
