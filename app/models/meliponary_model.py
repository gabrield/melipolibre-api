from app.database import db
from app.models.base import BaseModel

class Meliponary(db.Model, BaseModel):
    __tablename__ = 'meliponary'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    beekeeper_id    = db.Column(db.Integer, db.ForeignKey("beekeeper.id"), nullable=False)
    name            = db.Column(db.String(128), nullable=False)
    address         = db.Column(db.String(64), nullable=False)
 
    hives           = db.relationship("BeeHive", backref='meliponary')
    db.relationship("BeeHive", backref='beehive')


    def __repr__(self):
        return f'<Meliponary "{self.name}">' 
    