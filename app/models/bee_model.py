from app.database import db
from app.models.base_model import BaseModel

class BeeModel(db.Model, BaseModel):
    __tablename__ = 'bees'
    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genus           = db.Column(db.String(30))
    subgenus        = db.Column(db.String(30))
    specie          = db.Column(db.String(30), nullable=False)
    common_name     = db.Column(db.String(150))


    def __repr__(self):
        return f'<Bee "{self.specie}">'

