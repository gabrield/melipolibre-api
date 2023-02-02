import pytest
import factory
from tests.factories import BeeKeeperFactory

def test_create_beekeeper(client, beekeeper_stub):
    response = client.post("/v1/beekeepers", json=beekeeper_stub)
    assert response.status_code == 201


def test_create_beekeeper_with_short_password(client, beekeeper_stub):
    '''Password MUST BE at least 8 characters'''
    beekeeper_stub['password'] = '1234567'
    response = client.post("/v1/beekeepers", json=beekeeper_stub)
    assert response.status_code == 400


def test_create_beekeeper_without_email(client, beekeeper_stub):
    del beekeeper_stub['email']
    response = client.post("/v1/beekeepers", json=beekeeper_stub)

    assert response.status_code == 400


def test_create_beekeeper_without_password(client, beekeeper_stub):
    del beekeeper_stub['password']
    response = client.post('/v1/beekeepers', json=beekeeper_stub)

    assert response.status_code == 400

'''
#TO BE IMPLEMENTED
def test_update_beekeeper_name(client):
    ...

def test_update_beekeeper_email(client):
    ...

def test_update_beekeeper_password(client):
    ...

def test_update_beekeeper_with_invalid_credential(client):
    ...
'''