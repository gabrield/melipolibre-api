from flask_restx import Resource, reqparse, inputs
from flask_jwt_extended import jwt_required  # current_user
from app.database import db
from app.models.handling_model import HandlingModel

params = reqparse.RequestParser()
params.add_argument('beehive_id', type=int)
params.add_argument('handling', type=dict)
params.add_argument('handling_type', type=str)

# params.add_argument('password', type=password_type,
#                    required=True,
#                    help="A valid password required!",
#                    trim=True)


class Handlings(Resource):

    #@jwt_required()
    def get(self):
        return HandlingModel.query.all(), 201

    #@jwt_required()
    def post(self):
        _params = params.parse_args()
        print(_params)
        #MUST IMPLEMENT VALIDATIONS
        handling = HandlingModel(**_params)
        db.session.add(handling)
        db.session.commit()
        return {'message': f'{handling.handling_type} created.... '}, 201
        return {}, 201

    @jwt_required()
    def delete(self):
        ...
