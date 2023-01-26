import pytest
from app.models.beekeeper_model import BeeKeeperModel
from app.models.meliponary_model import MeliponaryModel
from app.models.beehive_model import BeeHiveModel, BeeHiveType
from app.models.bee_model import BeeModel

def test_create_one_beekeeper_model(db):
    beekeeper = BeeKeeperModel(name='Gabs', email='gabs@abelha.cc', password='123')
    db.session.add(beekeeper)
    db.session.commit()
    db.session.refresh(beekeeper)
    assert beekeeper.name == 'Gabs'