import pytest
import factory
from faker import Faker
from tests.factories import BeeKeeperFactory

def test_login_to_obtain_authorizarion_token(client):
    beekeeper = factory.build(dict, FACTORY_CLASS=BeeKeeperFactory)
    response = client.post("/v1/beekeepers", json=beekeeper)
    assert response.status_code == 201 #DRY CREATE AN ALREADY EXISTING BEEKEEPER

    response = client.post("/v1/login", json=beekeeper)

    assert response.status_code == 200
    assert response.json.get('access_token')
    assert len(response.json.get('access_token')) == 261 # JWT string-token length


def test_login_with_invalid_credentials(client):
    beekeeper = factory.build(dict, FACTORY_CLASS=BeeKeeperFactory)
    response = client.post("/v1/login", json=beekeeper)
    
    assert response.status_code == 401 #Unauthorized
    assert response.json == {'message' : 'Wrong user or password'}

def test_login_with_missing_email(client):
    beekeeper = factory.build(dict, FACTORY_CLASS=BeeKeeperFactory)
    del beekeeper['email']
    response = client.post('/v1/login', json=beekeeper)

    assert response.status_code == 400 #Bad request
    assert response.json == {
                        "errors": {
                            "email":
                            "An valid email address required! Missing required parameter"
                            " in the JSON body or the post body or the query string"
                        },
                        "message": "Input payload validation failed"
                    }

def test_login_with_missing_password(client):
    beekeeper = factory.build(dict, FACTORY_CLASS=BeeKeeperFactory)
    del beekeeper['password']
    response = client.post('/v1/login', json=beekeeper)

    assert response.status_code == 400
    assert response.json == {
                        "errors": {
                            "password": "Password required! Missing required parameter in the JSON body"
                            " or the post body or the query string"
                        },
                        "message": "Input payload validation failed"
                    }

def test_login_with_invalid_email(client):
    beekeeper = factory.build(dict, FACTORY_CLASS=BeeKeeperFactory)
    beekeeper['email'] =  Faker().email() +'@' +Faker().name()

    response = client.post('/v1/login', json=beekeeper)
    assert response.status_code == 400
    assert response.json == {
                    "errors": {
                        "email": "An valid email address required! {email} is not a"
                        " valid email".format(email=beekeeper.get('email'))
                    },
                    "message": "Input payload validation failed"
}





