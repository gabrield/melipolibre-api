import pytest
import factory
from app.models.beekeeper_model import BeeKeeperModel
from tests.factories import BeeKeeperFactory

def test_login_to_obtain_authorizarion_token(client, beekeeper):

    response = client.post("/v1/login", json=beekeeper)

    assert response.status_code == 200, "Expected code 200"
    assert response.json.get('access_token'), "No access token"
    assert len(response.json.get('access_token')) == 261 # JWT string-token length


def test_login_with_invalid_credentials(client, beekeeper_stub):
    response = client.post("/v1/login", json=beekeeper_stub)
    
    assert response.status_code == 401 #Unauthorized
    assert response.json == {'message' : 'Wrong user or password'}

def test_login_with_missing_email(client, beekeeper_stub):
    del beekeeper_stub['email']
    response = client.post('/v1/login', json=beekeeper_stub)

    assert response.status_code == 400 #Bad request
    assert response.json == {
                        "errors": {
                            "email":
                            "An valid email address required! Missing required parameter"
                            " in the JSON body or the post body or the query string"
                        },
                        "message": "Input payload validation failed"
                    }

def test_login_with_missing_password(client, beekeeper_stub):
    del beekeeper_stub['password']
    response = client.post('/v1/login', json=beekeeper_stub)

    assert response.status_code == 400
    assert response.json == {
                        "errors": {
                            "password": "Password required! Missing required parameter in the JSON body"
                            " or the post body or the query string"
                        },
                        "message": "Input payload validation failed"
                    }
def test_login_with_void_password(client, beekeeper):
    beekeeper['password'] = ''
    response = client.post('/v1/login', json=beekeeper)
    assert response.status_code == 401
    assert response.json == {'message': 'Wrong user or password'}


def test_login_with_invalid_email(client, beekeeper_stub):
    beekeeper_stub['email'] =  beekeeper_stub['email'] +'@' + beekeeper_stub['name']
    response = client.post('/v1/login', json=beekeeper_stub)
    assert response.status_code == 400, "Expected code 400"
    assert response.json == {
                    "errors": {
                        "email": "An valid email address required! {email} is not a"
                        " valid email".format(email=beekeeper_stub.get('email'))
                    },
                    "message": "Input payload validation failed"
}





