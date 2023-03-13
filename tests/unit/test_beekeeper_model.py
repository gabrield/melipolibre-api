import pytest, sqlalchemy
from app.models.beekeeper_model import BeeKeeperModel
from app.models.meliponary_model import MeliponaryModel
from app.models.beehive_model import BeeHiveModel, BeeHiveType
from app.models.bee_model import BeeModel
from factories import BeeKeeperFactory

def test_create_one_beekeeper_model(db):
    beekeeper = BeeKeeperFactory(name='Gabs', email='gabs@melipolibre.cc', password='123')
    assert beekeeper.name == 'Gabs'
    assert beekeeper.email == 'gabs@melipolibre.cc'
    assert beekeeper.password == '123'
    assert beekeeper.active == False

@pytest.mark.parametrize("name, email, password", [
    ('Gabs', 'gabs@melipolibre.cc', None),
    ("Test", None ,"name"),
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
