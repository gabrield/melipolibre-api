import os
from flask_restful import Api
from app.resources.bee import Bees
from app import create_app


config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
api = Api(app)
api.add_resource(Bees, '/bees')
#bee resources

    


if __name__ == '__main__':
    app.run()
