from app.database import db
from app.models.base_model import BaseModel
from app.models.beehive_model import BeeHiveModel


class MeliponaryModel(db.Model, BaseModel):
    __tablename__ = 'meliponaries'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    beekeeper_id    = db.Column(db.Integer, db.ForeignKey("beekeepers.id"), nullable=False)
    name            = db.Column(db.String(128), nullable=False)
    address         = db.Column(db.String(64), nullable=False)
    hives           = db.relationship("BeeHiveModel", backref='meliponary')


    def __repr__(self):
        return f'<Meliponary "{self.name}">' 
    