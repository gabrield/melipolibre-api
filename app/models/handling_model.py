from app.database import db
from app.models.base_model import BaseModel
from app.models.beehive_model import BeeHiveModel
from sqlalchemy_json import NestedMutableJson

class HandlingModel(db.Model):
    def __init__(self):
        __tablename__ = 'handlings'
        id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
        beehive_id = db.Column(db.Integer, db.ForeignKey('beehives.id'), nullable=False)
        handling   = db.Column(NestedMutableJson)
        beehive    = db.relationship("BeeHiveModel", backref='handlings', lazy='dynamic')
        created_at      = db.Column(db.String,  default=db.func.current_timestamp())
        updated_at      = db.Column(db.String,  default=db.func.current_timestamp(),
                                                onupdate=db.func.current_timestamp())