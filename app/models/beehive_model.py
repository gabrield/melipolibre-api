from sqlalchemy import ForeignKey
from app.database import db
from app.models.base import BaseModel
import enum
 
class BeeHiveType(enum.Enum):
    INPA   = 1
    BAU    = 2
    AF     = 3
    WF     = 4
    UNKNOW = 5

class BeeHive(db.Model, BaseModel):
    __tablename__ = 'beehive'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bee_id          = db.Column(db.Integer, db.ForeignKey('bee.id'), nullable=False)
    beekeeper_id    = db.Column(db.Integer, db.ForeignKey('beekeeper.id'), nullable=False)
    meliponary_id   = db.Column(db.Integer, db.ForeignKey('meliponary.id'), nullable=False)
    hive_type       = db.Column(db.Enum(BeeHiveType), nullable=False)
    bee             =  db.relationship('Bee', backref='bee')
