from app.database import db
#from sqlalchemy_utils import ScalarListType
from .base import BaseModel

class BeeModel(db.Model, BaseModel):
    __tablename__ = 'bees'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genus           = db.Column(db.String(60))
    subgenus        = db.Column(db.String(60))
    specie          = db.Column(db.String(60))
    common_name     = db.Column(db.String(350))
    occurrence_area = db.Column(db.String(150))


