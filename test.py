import pytest
from app import app

valid_json = {
    "age": 29.0,
    "checked": False,
    "description": "Student",
    "name": "John",
    "person_type": "English"
}
invalid_json = {
    "age": 12,
    "checked": False,
    "description": "Student",
    "person_type": "English"
}


@pytest.fixture(scope='module')
def client():
    with app.app.test_client() as c:
        yield c


# create test cases

def test_valid_create(client):
    client.delete('/persons/5')
    put_response = client.put('/persons/5', json=valid_json)
    get_response = client.get('/persons/5')
    assert put_response.status_code == 201
    assert get_response.status_code == 200

def test_invalid_create(client):
    client.delete('/persons/5')
    put_response = client.put('/persons/5', json=invalid_json)
    assert put_response.status_code == 400


# index test cases

def test_non_empty_index(client):
    client.delete('/persons/5')
    put_response = client.put('/persons/5', json=valid_json)
    get_response = client.get('/persons')
    
    assert put_response.status_code == 201
    # if person with id=5 is present
    assert len(list(filter(lambda x: x['id']==5, get_response.json))) == 1
    assert get_response.status_code == 200


def test_empty_index(client):
    client.delete('/persons/5')
    response = client.get('/persons')
    # if person with id=5 is still present after deletion
    assert len(list(filter(lambda x: x['id']==5,response.json))) == 0
    assert response.status_code == 200


# get test cases

def test_get_person(client):
    client.delete('/persons/5')
    put_response = client.put('/persons/5', json=valid_json)
    get_response = client.get('/persons/5')
    
    assert put_response.status_code == 201
    assert get_response.json['id'] == 5
    assert get_response.status_code == 200


def test_invalid_get_person(client):
    client.delete('/persons/5')
    response = client.get('/persons/5')
    assert response.status_code == 404




# delete cases

def test_valid_delete(client):
    put_response = client.put('/persons/5', json=valid_json)
    get_response1 = client.get('/persons/5')
    delete_response = client.delete('/persons/5')
    get_response2 = client.get('/persons/5')
    
    assert put_response.status_code == 201
    assert get_response1.status_code == 200
    assert delete_response.status_code == 204
    assert get_response2.status_code == 404

def test_invalid_delete(client):
    # delete if present
    response = client.delete('/persons/5')
    # invalid delete
    response = client.delete('/persons/5')
    assert response.status_code == 404