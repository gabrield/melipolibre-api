from flask_restx import Resource, reqparse, inputs, fields
from flask_jwt_extended import jwt_required  # current_user
from app.database import db
from app.blueprint_api import api
from app.models.handling_model import HandlingModel, HandlingType

params = reqparse.RequestParser()
params.add_argument('beehive_id', type=int, required=True)
params.add_argument('handling', type=dict, required=True)
params.add_argument('type', type=str, required=True)

# params.add_argument('password', type=password_type,
#                    required=True,
#                    help="A valid password required!",
#                    trim=True)
# handling_list = []
# handling_list.append({'type': 'INSPECTION'})

handling = api.model('Handlings', {
    'beehive_id': fields.Integer(min=0),
    'handling': fields.Raw(description='Handling dictionary containing \
                                        valid fields', required=True),
    'type': fields.String(description='Handling type',
                          enum=list(HandlingType))
})


class Handlings(Resource):

    #@jwt_required()
    def get(self):
        return HandlingModel.query.all(), 200

    #@jwt_required()
    @api.doc(body=handling)
    def post(self):
        _params = params.parse_args()
        print(_params)
        #MUST IMPLEMENT VALIDATIONS
        handling = HandlingModel(**_params)
        db.session.add(handling)
        db.session.commit()
        return {'Message': f'{handling.type} created.... '}, 201
        return {}, 201

    @jwt_required()
    def delete(self):
        ...
