from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = [
    {
        "id": 1, 
        "product_name": "Organic Almond Milk", 
        "brands": "Silk", 
        "quantity": 10,
        "ingredients_text": "Filtered water, almonds, cane sugar..."
    }
]

def fetch_product_from_api(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("status") == 1:
            return data["product"]
    except Exception:
        return None
    return None

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in inventory if i['id'] == item_id), None)
    return jsonify(item) if item else (jsonify({"error": "Not found"}), 404)

@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.json

    if "barcode" in data:
        api_data = fetch_product_from_api(data["barcode"])
        if api_data:
            new_item = {
                "id": len(inventory) + 1,
                "product_name": api_data.get("product_name", "Unknown"),
                "brands": api_data.get("brands", "Unknown"),
                "quantity": data.get("quantity", 1),
                "ingredients_text": api_data.get("ingredients_text", "")
            }
            inventory.append(new_item)
            return jsonify(new_item), 201
            
    new_item = {
        "id": len(inventory) + 1,
        "product_name": data.get("product_name"),
        "brands": data.get("brands"),
        "quantity": data.get("quantity", 0)
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.json
    item = next((i for i in inventory if i['id'] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    item.update({k: v for k, v in data.items() if k != "id"})
    return jsonify(item), 200

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    inventory = [i for i in inventory if i['id'] != item_id]
    return jsonify({"message": "Deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)