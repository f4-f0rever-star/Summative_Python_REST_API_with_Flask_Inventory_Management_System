import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    res = client.get('/inventory')
    assert res.status_code == 200
    assert isinstance(res.json, list)

def test_add_item(client):
    payload = {"product_name": "Test Apple", "quantity": 5}
    res = client.post('/inventory', json=payload)
    assert res.status_code == 201
    assert res.json['product_name'] == "Test Apple"