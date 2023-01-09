from app.database import db
from app.models.base import BaseModel

class Bee(db.Model, BaseModel):
    __tablename__ = 'bee'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genus           = db.Column(db.String(30))
    subgenus        = db.Column(db.String(30))
    specie          = db.Column(db.String(30), nullable=False)
    common_name     = db.Column(db.Unicode(150))

