import pytest
from app.models.planet import Planet

def test_get_planets_is_empty(client):
    response = client.get('/planets')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_planets_works_with_two_planets(client,two_saved_planets):
    response = client.get('/planets')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "name": "Ocean World",
            "description": "watr 4evr",
            "population": 292929
        },
        {
            "id": 2,
            "name": "Mountain World",
            "description": "i luv 2 climb rocks",
            "population": 123456789
        }
    ]

def test_get_one_planet_no_planets(client):
    response = client.get('planets/1')
    response_body = response.get_json()

    assert response.status_code == 404
    assert "message" in response_body
    assert response_body['message'] == "Planet with ID 1 not in solar system"

def test_get_one_planet_with_two_planets(client,two_saved_planets):
    response = client.get('planets/1')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
            "id": 1,
            "name": "Ocean World",
            "description": "watr 4evr",
            "population": 292929
        }

def test_post_one_planet_with_json(client):
    the_json = {
            "name": "Cheese World",
            "description": "lactose 4evr",
            "population": 9001
        }
    response = client.post('/planets', json = the_json)
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == "Planet Cheese World was created"

    response2 = client.get('planets/1')
    response_body2 = response2.get_json()

    assert response2.status_code == 200
    assert response_body2 == {
            "id": 1,
            "name": "Cheese World",
            "description": "lactose 4evr",
            "population": 9001
        }