import pytest
import sqlalchemy
from app.models.beekeeper_model import BeeKeeperModel
from app.models.meliponary_model import MeliponaryModel
from app.models.beehive_model import BeeHiveModel, BeeHiveType
from app.models.bee_model import BeeModel
from factories import BeeKeeperFactory

@pytest.mark.parametrize("name, email, password", [
    ('Gabs', 'gabs@melipolibre.cc', None),
    ("Test", None, "name"),
    (None, None, 'pwdtest'),
    (None, None, None),
    ("Daniel", None, None)
])
def test_create_beekeeper_with_missing_parameters(db, name, email, password):
    '''Must raise an exception by miscreating BeeKeeperModel'''
    with pytest.raises(sqlalchemy.exc.IntegrityError) as e:
        beekeeper = BeeKeeperModel(name=name, email=email, password=password)
        db.session.add(beekeeper)
        db.session.commit()


def test_create_one_beekeeper_model_and_save_to_db(db):
    try:
        beekeeper = BeeKeeperModel(
            name='Gabs', email='gabs@melipolibre.cc', password='11111')
        db.session.add(beekeeper)
        db.session.commit()
    except Exception:
        raise Exception("test_create_one_beekeeper_model_and_save_to_db")


def test_create_one_beekeeper_and_retrieve_from_db(db):
    beekeeper = BeeKeeperFactory()
    assert db.session.query(BeeKeeperModel).filter(
        BeeKeeperModel.email == beekeeper.email).one() == beekeeper


'''
tests to be added on this file

update_beekeeper properties
update_beekeeper properties with invalid input (missing or out of format)
delete beekeeper


'''
