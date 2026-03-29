import pytest
from app import app, inventory

@pytest.fixture
def client():
    """Sets up a test client for the Flask app"""
    app.config['TESTING'] = True
    inventory.clear()
    inventory.append({"id": 1, "product_name": "Initial Item", "quantity": 5})
    with app.test_client() as client:
        yield client

def test_get_all_inventory(client):
    """Test GET /inventory"""
    response = client.get('/inventory')
    assert response.status_code == 200
    assert len(response.json) == 1

def test_add_item_manual(client):
    """Test POST /inventory (Manual)"""
    new_item = {"product_name": "Bread", "quantity": 2}
    response = client.post('/inventory', json=new_item)
    assert response.status_code == 201
    assert response.json['product_name'] == "Bread"

def test_update_item(client):
    """Test PATCH /inventory/<id>"""
    update_data = {"quantity": 50}
    response = client.patch('/inventory/1', json=update_data)
    assert response.status_code == 200
    assert response.json['quantity'] == 50

def test_delete_item(client):
    """Test DELETE /inventory/<id>"""
    response = client.get('/inventory')
    initial_count = len(response.json)
    
    client.delete('/inventory/1')
    
    response_after = client.get('/inventory')
    assert len(response_after.json) == initial_count - 1

from unittest.mock import patch

@patch('app.requests.get')
def test_add_via_barcode_mock(mock_get, client):
    """Tests adding an item using a fake OpenFoodFacts response"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Mocked Milk",
            "brands": "Test Brand",
            "ingredients_text": "Water, Soy"
        }
    }

    payload = {"barcode": "123456", "quantity": 10}
    response = client.post('/inventory', json=payload)
    
    assert response.status_code == 201
    assert response.json['product_name'] == "Mocked Milk"
    assert response.json['brands'] == "Test Brand"