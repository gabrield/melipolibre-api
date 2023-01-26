import pytest, json
from app.models.beekeeper_model import BeeKeeperModel
from app.models.meliponary_model import MeliponaryModel
from app.models.beehive_model import BeeHiveModel, BeeHiveType
from app.models.bee_model import BeeModel

def test_create_one_beekeeper(client):
    response = client.post("/v1/beekeepers", json={
        "name": "sdfsdfsd",
        "email" : "gabs12@gmail.com",
        "password": "23423421"
    })
    assert response.status_code == 201


def test_login_to_obtain_valid_authorizarion_token(client):
    response = client.post("/v1/beekeepers", json={
        "name": "sdfsdfsd",
        "email" : "gabs12@gmail.com",
        "password": "23423421"
    })

    assert response.status_code == 201

    response = client.post("/v1/login", json={
        "name": "sdfsdfsd",
        "email" : "gabs12@gmail.com",
        "password": "23423421"
    })
    token = json.loads(response.data)
    assert 'access_token' in token
    assert bool(token['access_token'].strip())