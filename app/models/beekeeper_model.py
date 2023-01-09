from app.database import db
from app.models.base import BaseModel

class BeeKeeper(db.Model, BaseModel):
    __tablename__ = 'beekeeper'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(128), nullable=False)
    email           = db.Column(db.String(64), nullable=False)
    password        = db.Column(db.String(30), nullable=False)
    api_key         = db.Column(db.String(150), nullable=False)
    meliponaries    = db.relationship('Meliponary', backref='beekeeper')
    hives           = db.relationship('BeeHive', backref='beekeeper')



