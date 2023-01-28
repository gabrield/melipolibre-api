import pytest
import factory
import json
from tests.factories import BeeKeeperFactory

def test_create_beekeeper(client):
    beekeeper = factory.build(dict, FACTORY_CLASS=BeeKeeperFactory)
    response = client.post("/v1/beekeepers", json=beekeeper)
    assert response.status_code == 201

#TO BE IMPLEMENTED
def test_create_beekeeper_without_email(client):
    ...

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