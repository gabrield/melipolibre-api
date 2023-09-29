from flask_restx import Resource, reqparse, inputs, fields
from flask_jwt_extended import jwt_required, current_user
from app.database import db
from app.blueprint_api import api
from app.models.handling_model import HandlingModel, HandlingType


validators = {}


def inspection(handling: dict):
    return True


def feeding(handling: dict):
    return True


def hive_change(handling: dict):
    return True


def transposition(handling: dict):
    return True


def split(handling: dict):
    return True


def add_validator(validator_dict: dict, handling: str):
    try:
        handling_validator = eval(handling.lower())
    except NameError:
        raise NameError(
            f'You must provide a function called {handling.lower()} before trying to add a validator')
    if not callable(handling_validator):
        raise NameError(
            f'You must provide a callable function called {handling.lower()} before trying to add a validator')

    validator_dict[handling] = handling_validator


for handling_type in list(HandlingType):
    add_validator(validators, handling_type)


def handling_type(type: str):
    if type not in list(HandlingType):
        raise ValueError('Unknow handling type')
    return type


params = reqparse.RequestParser()
params.add_argument('beehive_id', type=int, required=True)
params.add_argument('handling', type=dict, required=True)
params.add_argument('type', type=handling_type, required=True)


handling = api.model('Handlings', {
    'beehive_id': fields.Integer(min=0),
    'handling': fields.Raw(description='Handling dictionary containing \
                                        valid fields', required=True),
    'type': fields.String(description='Handling type',
                          enum=list(HandlingType))
})


class Handlings(Resource):
    @jwt_required()
    def get(self):
        return {'handlings': [handling.json() for hive in current_user.hives for handling in hive.handlings]}, 200

    @jwt_required()
    @api.doc(body=handling)
    def post(self):
        _params = params.parse_args()
        print(_params)

        (handling_validator) = validators[_params['type']]

        if handling_validator(_params['handling']):
            print(handling_validator)
            handling = HandlingModel(**_params)
            print(handling)
            db.session.add(handling)
            db.session.commit()
            return {'message': f'{handling.type} created.... '}, 201

        return {'message': f'{handling.type} not created.... '}, 401


class Handling(Resource):

    @jwt_required()
    def get(self):
        # return [handling for hive in current_user.hives for handling in hive.handlings] ???
        handlings = []

        for hive in current_user.hives:
            for handling in hive.handlings:
                handlings.append(handling)

        return {
            'handlings': handlings
        }, 200

    @jwt_required()
    @api.doc(body=handling)
    @jwt_required()
    def delete(self):
        ...
