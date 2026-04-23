# Summative_Python_REST_API_with_Flask_Inventory_Management_System
A robust REST API and Command-Line Interface designed to manage retail inventory. This system integrates with the **OpenFoodFacts API** to automatically supplement product details using barcodes.

## Features
* **Full CRUD API**: Create, Read, Update, and Delete inventory items via Flask.
* **External API Integration**: Fetch real-time data (names, brands, ingredients) from OpenFoodFacts.
* **Interactive CLI**: A user-friendly terminal interface for employees to manage stock.
* **Automated Testing**: Comprehensive suite using `pytest`


## Instructions
* **1. Clone the repository**
git clone git@github.com:f4-f0rever-star/Summative_Python_REST_API_with_Flask_Inventory_Management_System.git
navigate to the repo after cloning
* **2. Install dependencies**
pipenv install
* **3. Create virtual environment**
pipenv shell
## Run the application
python3 app.py 
## For CLI Usage
Open a new terminal while the app one is running still
create virtual environment
run the cli.py by using python3 cli.py

## Run all test using pytest