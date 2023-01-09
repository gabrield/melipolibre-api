from app.database import db
from app.models.base import BaseModel

class MeliponaryModel(db.Model, BaseModel):
    __tablename__ = 'meliponary'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(128), nullable=False)
    address         = db.Column(db.String(64), nullable=False)
    beekeeper_id    = db.Column(db.Integer, nullable=False)

