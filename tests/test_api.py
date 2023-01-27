import pytest
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

    assert response.status_code == 200
    assert response.json.get('access_token')
    assert len(response.json.get('access_token')) == 261 # JWT string-token length

def test_login_without_valid_credentials(client):
    response = client.post("/v1/login", json={
        "name": "sdfsdfsd",
        "email" : "gabs12@gmail.com",
        "password": "23423421"
    })
    
    assert response.status_code == 401 #Unauthorized
    assert response.json == {'message' : 'Wrong user or password'}

def test_create_user_with_missing_email(client):
    response = client.post('/v1/login', json={
        "name" : "gabs12",
        "password": "23423421"
    })

    assert response.status_code == 400
    assert response.json == {
                        "errors": {
                            "email":
                            "An valid email address required! Missing required parameter"
                            " in the JSON body or the post body or the query string"
                        },
                        "message": "Input payload validation failed"
                    }