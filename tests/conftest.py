import pytest
from app import create_app
from app.database import db as _db
from app.models.bee_model import BeeModel
import os, json

@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    with app.test_client() as client:
         with app.app_context():
            _db.drop_all()
            _db.create_all()
            yield client


@pytest.fixture
def db(app):
    app.app_context().push()
    _db.init_app(app)
    _db.create_all()
    with open(os.path.dirname(os.path.abspath(__file__)) + \
            '/data/asf_list.json', encoding='utf-8') as bee_file:
            bees =  json.load(bee_file)
            db.session.bulk_save_objects([BeeModel(**bee) for bee in bees])
            db.session.commit()
    yield _db
    _db.session.close()
    _db.drop_all()