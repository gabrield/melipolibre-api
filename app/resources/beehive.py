from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from app import filters
from app.database import db
from app.models.bee_model import BeeModel
from app.models.beehive_model import BeeHiveModel
from app.models.meliponary_model import MeliponaryModel

params = reqparse.RequestParser()
params.add_argument('bee_id', type=int, required=True)
params.add_argument('meliponary_id', type=int, required=True)



class BeeHives(Resource):
    @jwt_required()
    def get(self):
        return {
                'beehives':
                [beehive.json() for beehive in current_user.hives]
            }, 200
    
    def post(self):
        _params = params.parse_args()
        valid_params = filters.valid_req_params(_params)
        _bee = BeeModel.query.filter_by(id=valid_params['bee_id']).first()
        _meliponary = current_user.meliponaries.query.filter_by(id=valid_params['meliponary_id']).first()

        if _bee and _meliponary:
            new_hive = BeeHiveModel(bee=_bee, meliponary=_meliponary,
                                               beekeeper=current_user)
            db.session.add(new_hive)
            db.session.commit()
            return {'message' : f'Hive id:{new_hive.id} for {new_hive.bee.specie} created!'}, 201
        
        return {'message' : f'Could not create Beehive. Bee or Meliponary ID wrong'}, 403
