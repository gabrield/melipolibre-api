import pytest
from app.models.beekeeper_model import BeeKeeperModel
from app.models.meliponary_model import MeliponaryModel
from app.models.beehive_model import BeeHiveModel, BeeHiveType
from app.models.bee_model import BeeModel
from factories import BeeKeeperFactory

def test_create_one_beekeeper_model(db):
    beekeeper = BeeKeeperFactory(name='Gabs', email='gabs@abelha.cc', password='123')
    assert beekeeper.name == 'Gabs'
    assert beekeeper.email == 'gabs@abelha.cc'
    assert beekeeper.password == '123'
    assert beekeeper.active == False