import json
from flask_restx import Resource, reqparse, inputs
from app.models.beekeeper_model import BeeKeeperModel



class BeeKeeperRegister(Resource):
        params = reqparse.RequestParser()
        params.add_argument('name', type=str, required=True, help="name required" \
            trim=True))
        params.add_argument('email', type=inputs.email(dns=True), required=True, \
            help="valid email address required", trim=True)
        params.add_argument('password', type=str, required=True, help="password required" \
            trim=True))
        def get(self):
            params = BeeKeeperRegister.params.parse_args()
            pass