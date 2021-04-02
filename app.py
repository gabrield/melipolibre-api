from flask import Flask
from flask_restful import Api
from resources.bee import Bee, Bees
from models.bee import BeeModel
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nativasf.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
api = Api(app)

@app.before_first_request
def create_database():
    db.drop_all()
    db.create_all()
    with open('asf_list.json') as bee_file:
        bees =  json.load(bee_file)
        db.session.bulk_save_objects([BeeModel(**bee) for bee in bees])
        db.session.commit()
    

#bee resources
api.add_resource(Bees, '/bees')
#api.add_resource(Bee, '/bee')


if __name__ == '__main__':
    from database import db

    db.init_app(app)
    app.run(debug=True)



