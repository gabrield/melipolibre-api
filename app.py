import os
from flask_restful import Api
from app.resources.bee import Bees
from app import create_app


app = create_app()
api = Api(app)

api.add_resource(Bees, '/bees')

if __name__ == '__main__':
    app.run()
