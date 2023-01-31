from app.database import db
from app.models.base_model import BaseModel
from app.models.meliponary_model import MeliponaryModel
from app.models.beehive_model import BeeHiveModel
from sqlalchemy_utils import force_auto_coercion
from sqlalchemy_utils.types.password import PasswordType

force_auto_coercion()

class BeeKeeperModel(db.Model, BaseModel):
    __tablename__ = 'beekeepers'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(128))
    email           = db.Column(db.String(64), nullable=False)
    password        = db.Column(PasswordType(schemes=['bcrypt']), nullable=False)
    active          = db.Column(db.Boolean, default=False)
    meliponaries    = db.relationship('MeliponaryModel', backref='beekeeper',
                                                         cascade="all, delete-orphan",
                                                         lazy='dynamic',
                                                         passive_deletes=True)
    hives           = db.relationship('BeeHiveModel', backref='beekeeper', lazy='dynamic')
    created_at      = db.Column(db.String, default=db.func.current_timestamp())


    def __repr__(self):
        return f'<BeeKeeper "{self.name}">'



