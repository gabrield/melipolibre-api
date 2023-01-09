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

class BeeColonyModel(db.Model, BaseModel):
    __tablename__ = 'beecolony'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bee_id          = db.Colum(db.Integer, required=True)
    beekeeper_id    = db.Colum(db.Integer, required=True)
    meliponary_id   = db.Colum(db.Integer)
    hive_type       = db.Column(db.Enum(BeehiveType))


