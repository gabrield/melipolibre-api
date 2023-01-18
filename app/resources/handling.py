from flask_restx import Resource
from flask_jwt_extended import jwt_required, current_user


class Handlings(Resource):

    @jwt_required()
    def get(self):
        ...

    @jwt_required()
    def put(self):
        ...

    @jwt_required()
    def delete(self):
        ...