from email.policy import default
from app.database import db
from app.models.base_model import BaseModel
from app.models.meliponary_model import MeliponaryModel
from app.models.beehive_model import BeeHiveModel


class BeeKeeperModel(db.Model, BaseModel):
    __tablename__ = 'beekeepers'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(128), nullable=False)
    email           = db.Column(db.String(64), nullable=False)
    password        = db.Column(db.String(30), nullable=False)
    api_key         = db.Column(db.String(256))
    active          = db.Column(db.Boolean, default=False)
    meliponaries    = db.relationship('MeliponaryModel', backref='beekeeper')
    hives           = db.relationship('BeeHiveModel', backref='beekeeper')

    def __repr__(self):
        return f'<BeeKeeper "{self.name}">'



