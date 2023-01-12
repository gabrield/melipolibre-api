import json
from flask_restx import Resource, reqparse, inputs
from app.database import db
from app.models.beekeeper_model import BeeKeeperModel
from app import filters



class BeeKeeperRegister(Resource):
        params = reqparse.RequestParser()
        params.add_argument('name', type=str, required=True, help='Name required!', \
            trim=True)
        params.add_argument('email', type=inputs.email(), required=True, \
            help="An valid email address required!", trim=True)
        params.add_argument('password', type=str, required=True, help="Password required!", \
            trim=True)

        def post(self):
            params = BeeKeeperRegister.params.parse_args()
            valid_params = filters.valid_req_params(params)
            print(valid_params['email'])
            beekeeper = BeeKeeperModel.query.filter(BeeKeeperModel.email == valid_params['email']).first()
            

            if beekeeper:
                return {'message': 'user already registered'}, 409

            try:
                beekeeper = BeeKeeperModel(**valid_params)
                db.session.add(beekeeper)
                db.session.commit()
                return {'message' : f'{beekeeper.email} created.... Check your email for activaction'}, 201
            except Exception as ex:
                return {'message' : ex}, 500