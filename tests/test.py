# APP_SETTINGS=development flask shell < test.py
from app import create_app
from flask import Blueprint
from flask_restx import Api
from app.database import db

from app.models.beekeeper_model import BeeKeeperModel
from app.models.meliponary_model import MeliponaryModel
from app.models.beehive_model import BeeHiveModel, BeeHiveType
from app.models.bee_model import BeeModel
import json
import os

app = create_app()
api = Api(app)
db.drop_all()
db.create_all()

with open('app/data/asf_list.json') as bee_file:
    bees =  json.load(bee_file)
    db.session.bulk_save_objects([BeeModel(**bee) for bee in bees])
    db.session.commit()

bk1 = BeeKeeperModel(name='Gabs', email='gabs@abelha.cc', password='123')
bk2 = BeeKeeperModel(name='Carlo', email='carlo@abelha.cc', password='123')

db.session.add(bk1, bk2)
db.session.commit()

bee1 = BeeModel.query.filter(BeeModel.specie.contains('angustula angustula')).first()
bee2 = BeeModel.query.filter(BeeModel.specie.contains('Melipona')).first()

mlp1 = MeliponaryModel(name='Meliponario 1', address='Felipe Camarão', beekeeper=bk1)
mlp2 = MeliponaryModel(name='Meliponario 2', address='Felipe Camarão 1', beekeeper=bk1)

hive1 = BeeHiveModel(bee=bee1, beekeeper=bk1, meliponary=mlp1, hive_type=BeeHiveType.INPA)
hive2 = BeeHiveModel(bee=bee2, beekeeper=bk1, meliponary=mlp2, hive_type=BeeHiveType.LANGSTROTH)
hive3 = BeeHiveModel(bee=bee2, beekeeper=bk2, meliponary=mlp2, hive_type=BeeHiveType.WF)

db.session.add_all([mlp1, mlp2])
db.session.add_all([hive1, hive2, hive3])
db.session.commit()
print(bk1.hives)
print(mlp1.hives)
print(mlp2.hives)
print(hive1.meliponary == mlp1)
print(hive1.meliponary == mlp2)
print(hive1.beekeeper)
print(hive2.beekeeper)
print(hive3.beekeeper)



print()

