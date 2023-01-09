from sqlalchemy import ForeignKey
from app.database import db
from app.models.base import BaseModel
import enum
 
class BeehiveType(enum.Enum):
    INPA   = 1
    BAU    = 2
    AF     = 3
    WF     = 4
    UNKNOW = 5

class BeeColony(db.Model, BaseModel):
    __tablename__ = 'beecolony'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bee_id          = db.Column(db.Integer, db.ForeignKey('bee.id'))
    beekeeper_id    = db.Column(db.Integer, db.ForeignKey('beepeeker.id'))
    meliponary_id   = db.Column(db.Integer, db.ForeignKey('meliponary.id'))
    hive_type       = db.Column(db.Enum(BeehiveType))


