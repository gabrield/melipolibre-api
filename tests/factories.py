import factory
from app.database import db as _db
from app.models.bee_model import BeeModel
from app.models.beehive_model import BeeHiveModel, BeeHiveType
from app.models.beekeeper_model import BeeKeeperModel
from app.models.meliponary_model import MeliponaryModel


class BeeKeeperFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = BeeKeeperModel
        sqlalchemy_session = _db.session
        sqlalchemy_session_persistence = 'commit'
    name = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class MeliponaryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = MeliponaryModel
        sqlalchemy_session = _db.session
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('name')
    address = factory.Faker('address')
    beekeeper = factory.SubFactory(BeeKeeperFactory)


class BeeHiveFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = BeeHiveModel
        sqlalchemy_session = _db.session
        sqlalchemy_session_persistence = 'commit'

    def __bee_generator(self):
        """Turn `BeeModel.query.all()` into a lazily evaluated generator"""
        yield BeeModel.query.all()

    beekeeper = factory.SubFactory(BeeKeeperFactory)
    meliponary = factory.SubFactory(MeliponaryFactory)
    bee = factory.Iterator(__bee_generator)
    hive_type = factory.Iterator(BeeHiveType)
