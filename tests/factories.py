import factory
from faker import Faker
from app.database import db
from app.models.beekeeper_model import BeeKeeperModel

faker = Faker()

class BeeKeeperFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = BeeKeeperModel
        sqlalchemy_session = db.session

    name = faker.name()
    email = faker.email()
    password = faker.password(length=12)