from enum import Enum, unique
from app.database import db
from app.models.base_model import BaseModel
from app.models.beehive_model import BeeHiveModel
from sqlalchemy_json import NestedMutableJson

@unique
class HandlingType(str, Enum):
    FEEDING        = 'FEEDING'
    HIVE_CHANGE    = 'HIVE_CHANGE'
    TRANSPOSITION  = 'TRANSPOSITION'
    SPLIT          = 'SPLIT'
    INSPECTION     = 'INSPECTION'
    #CHECKS IF STRING IS IN HandlingType print('FEEDING' in list(HandlingType))

class HandlingModel(db.Model):
    def __init__(self):
        __tablename__ = 'handlings'
        id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
        beehive_id    = db.Column(db.Integer, db.ForeignKey('beehives.id'), nullable=False)
        handling      = db.Column(NestedMutableJson, nullable=False)
        handling_type = db.Column(db.Enum(HandlingType), nullable=False)
        beehive       = db.relationship("BeeHiveModel", backref='handlings', lazy='dynamic')
        created_at    = db.Column(db.String,  default=db.func.current_timestamp())
        updated_at    = db.Column(db.String,  default=db.func.current_timestamp(),
                                                onupdate=db.func.current_timestamp())