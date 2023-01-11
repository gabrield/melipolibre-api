from sqlalchemy import ForeignKey
from app.database import db
from app.models.base_model import BaseModel
import enum
 
class BeeHiveType(enum.Enum):
    INPA   = 1
    BAU    = 2
    AF     = 3
    WF     = 4
    LANGSTROTH = 5
    UNKNOW = 6


class BeeHiveModel(db.Model, BaseModel):
    __tablename__ = 'beehives'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bee_id          = db.Column(db.Integer, db.ForeignKey('bees.id'), nullable=False)
    beekeeper_id    = db.Column(db.Integer, db.ForeignKey('beekeepers.id'), nullable=False)
    meliponary_id   = db.Column(db.Integer, db.ForeignKey('meliponaries.id'), nullable=False)
    hive_type       = db.Column(db.Enum(BeeHiveType), nullable=False)
    bee             = db.relationship('BeeModel', backref='bee')

    def __repr__(self):
        return f'<BeeHive "{self.bee.specie}">'



