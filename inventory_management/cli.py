import requests

BASE_URL = "http://127.0.0.1:5000/inventory"

def main_menu():
    print("\n--- Inventory Manager ---")
    print("1. View All Inventory")
    print("2. Add Item (Manual)")
    print("3. Add Item (via Barcode)")
    print("4. Update Item Quantity")
    print("5. Delete Item")
    print("6. Exit")
    return input("Select an option: ")

def view_all():
    response = requests.get(BASE_URL)
    for item in response.json():
        print(f"[{item['id']}] {item['product_name']} - Brand: {item.get('brands')} - Stock: {item['quantity']}")

def add_by_barcode():
    barcode = input("Enter product barcode: ")
    qty = int(input("Initial quantity: "))
    payload = {"barcode": barcode, "quantity": qty}
    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 201:
        print("Product fetched and added successfully!")
    else:
        print("Error: Could not find product or add to inventory.")

def update_stock():
    item_id = input("Enter Item ID to update: ")
    new_qty = int(input("Enter new quantity: "))
    response = requests.patch(f"{BASE_URL}/{item_id}", json={"quantity": new_qty})
    print("Update successful!" if response.status_code == 200 else "Update failed.")

def delete_item():
    item_id = input("Enter Item ID to delete: ")
    requests.delete(f"{BASE_URL}/{item_id}")
    print("Item removed.")

if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == "1": view_all()
        elif choice == "2": 
            name = input("Name: ")
            requests.post(BASE_URL, json={"product_name": name, "quantity": 0})
        elif choice == "3": add_by_barcode()
        elif choice == "4": update_stock()
        elif choice == "5": delete_item()
        elif choice == "6": break