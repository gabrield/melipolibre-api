from app.database import db
from app.models.beekeeper_model import BeeKeeper
from app.models.meliponary_model import Meliponary
from app.models.beehive_model import BeeHive, BeeHiveType
from app.models.bee_model import Bee
import json
import os

db.drop_all()
db.create_all()

with open('app/data/asf_list.json') as bee_file:
    bees =  json.load(bee_file)
    #print(bees)
    db.session.bulk_save_objects([Bee(**bee) for bee in bees])
    db.session.commit()

bk1 = BeeKeeper(name='Gabs', email='gabs@abelha.cc', password='123', api_key='342sdvsfds')
db.session.add(bk1)
db.session.commit()
bee1 = Bee.query.filter(Bee.specie.contains('angustula angustula')).first()
mlp1 = Meliponary(name='Casa 1', address='Felipe Camarão', beekeeper=bk1)
mlp2 = Meliponary(name='Casa 2', address='Felipe Camarão 1', beekeeper=bk1)
hive1 = BeeHive(bee=bee1, beekeeper=bk1, meliponary=mlp1, hive_type=BeeHiveType.INPA)
hive2 = BeeHive(bee=bee1, beekeeper=bk1, meliponary=mlp1, hive_type=BeeHiveType.INPA)


db.session.add(mlp1)
db.session.add(mlp2)
db.session.add(hive1)
db.session.add(hive2)
db.session.commit()
print(bk1.hives)
print(mlp1.hives)
print(hive1.meliponary == mlp1)
print(hive1.bee.json())

print()

#for meliponary in bk1.meliponaries:
#    print(meliponary.json())


