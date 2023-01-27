import pytest
import factory
import json
from tests.factories import BeeKeeperFactory

def test_create_one_new_beekeeper(client):
    beekeeper = factory.build(dict, FACTORY_CLASS=BeeKeeperFactory)
    response = client.post("/v1/beekeepers", json=beekeeper)
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

def test_create_user_with_missing_password(client):
    response = client.post('/v1/login', json={
        "name" : "gabs12",
        "email": "email@email.com"
    })

    assert response.status_code == 400
    assert response.json == {
                        "errors": {
                            "password": "Password required! Missing required parameter in the JSON body"
                            " or the post body or the query string"
                        },
                        "message": "Input payload validation failed"
                    }
def test_create_user_with_invalid_email(client):
    invalid_email =  'email.email.com'
    response = client.post('/v1/login', json={
        "name" : "gabs12",
        "password" : "sasd3423",
        "email": invalid_email
    })

    assert response.status_code == 400
    assert response.json == {
                        "errors": {
                            "email": f'An valid email address required! {invalid_email} is not a valid email'
                        },
                        "message": "Input payload validation failed"
                    }


def test_update_user(client):
    ...


def test_update_user_name(client):
    ...

def test_update_user_email(client):
    ...

def test_update_user_password(client):
    ...

def test_update_user_with_invalid_credential(client):
    ...



