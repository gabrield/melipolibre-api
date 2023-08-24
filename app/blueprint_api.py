
from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint('melipolibre-api', __name__)
api = Api(blueprint)