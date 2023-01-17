from enum import Enum, unique
from sqlalchemy import ForeignKey
from app.database import db
from app.models.base_model import BaseModel
from app.models.bee_model import BeeModel


@unique
class BeeHiveType(str, Enum):
    INPA   = 'INPA'
    BAU    = 'BAU'
    AF     = 'AF'
    WF     = 'WF'
    LANGSTROTH = 'LANGSTROTH'
    UNKNOW = 'UNKNOW'


class BeeHiveModel(db.Model, BaseModel):
    __tablename__ = 'beehives'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bee_id          = db.Column(db.Integer, db.ForeignKey('bees.id'), nullable=False)
    beekeeper_id    = db.Column(db.Integer, db.ForeignKey('beekeepers.id'), nullable=False)
    meliponary_id   = db.Column(db.Integer, db.ForeignKey('meliponaries.id'), nullable=False)
    hive_type       = db.Column(db.Enum(BeeHiveType), nullable=False)
    bee             = db.relationship('BeeModel', backref='bee')

    created_at      = db.Column(db.String,  default=db.func.current_timestamp())
    updated_at      = db.Column(db.String,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<BeeHive "{self.bee.specie}">'



