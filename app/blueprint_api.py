
from flask import Blueprint
from flask_restx import Api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'body',
        'name': 'Authorization'
    }
}


blueprint = Blueprint('melipolibre-api', __name__)
api = Api(blueprint,
          title='Melipolibre RESTFul API',
          default="Melipolibre RESTFul routes",
          default_label=" API to handle Melipolibre's data",
          version='v0.1',
          authorizations=authorizations)

