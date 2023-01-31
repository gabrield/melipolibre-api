import pytest
import factory
from tests.factories import BeeKeeperFactory

def test_create_beekeeper(client):
    beekeeper = BeeKeeperFactory.build().json()
    response = client.post("/v1/beekeepers", data=beekeeper)
    assert response.status_code == 201


def test_create_beekeeper_without_email(client):
    beekeeper = BeeKeeperFactory.build().json()
    del beekeeper['email']
    response = client.post("/v1/beekeepers", data=beekeeper)

    assert response.status_code == 400
    assert response.json == {
                        "errors": {
                            "email":
                            "An valid email address required! Missing required parameter"
                            " in the JSON body or the post body or the query string"
                        },
                        "message": "Input payload validation failed"
            }

'''
#TO BE IMPLEMENTED
def test_create_beekeeper_without_password(client):

     ...

def test_update_beekeeper_name(client):
    ...

def test_update_beekeeper_email(client):
    ...

def test_update_beekeeper_password(client):
    ...

def test_update_beekeeper_with_invalid_credential(client):
    ...
'''