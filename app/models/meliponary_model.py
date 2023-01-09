from app.database import db
from app.models.base import BaseModel

class Meliponary(db.Model, BaseModel):
    __tablename__ = 'meliponary'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(128), nullable=False)
    address         = db.Column(db.String(64), nullable=False)
    beekeeper_id    = db.Column(db.Integer, db.ForeignKey("beekeeper.id"), nullable=False)


    db.relationship("beekeeper", backref='meliponary')

