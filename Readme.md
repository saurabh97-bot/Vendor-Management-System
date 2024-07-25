# Vendor Management System with Performance Metrics
This is a Django-based Vendor Management System REST API project for managing vendors and purchase orders. 
The API provides endpoints for creating, reading, updating, and deleting vendors and purchase orders, 
as well as retrieving performance metrics for vendors.

## Features

* Vendor management: create, read, update, and delete vendors
* Purchase order management: create, read, update, and delete purchase orders
* Performance metrics: retrieve performance metrics for vendors
* Acknowledge purchase orders: acknowledge purchase orders

## API Endpoints

The API provides the following endpoints:

### Vendor Endpoints

* `GET /api/vendors/`: List all vendors
* `POST /api/vendors/`: Create a new vendor
* `GET /api/vendors/{vendor_id}/`: Retrieve a specific vendor
* `PUT /api/vendors/{vendor_id}/`: Update a vendor
* `DELETE /api/vendors/{vendor_id}/`: Delete a vendor

### Purchase Order Endpoints

* `GET /api/purchase_orders/`: List all purchase orders
* `POST /api/purchase_orders/`: Create a new purchase order
* `GET /api/purchase_orders/{po_id}/`: Retrieve a specific purchase order
* `PUT /api/purchase_orders/{po_id}/`: Update a purchase order
* `DELETE /api/purchase_orders/{po_id}/`: Delete a purchase order

### Performance Metrics Endpoints

* `GET /api/vendors/{vendor_id}/performance/`: Retrieve a vendor's performance metrics

### Acknowledge Purchase Order Endpoint

* `POST /api/purchase_orders/{po_number}/acknowledge/`: Acknowledge a purchase order

### Admin Username Password
* Admin: Vendor
* Password: 123456

## Setup Instructions

1. Clone the repository: `git clone https://github.com/your-username/django-rest-api.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a virtual environment: `virtualenv venv -p python3`
4. Activate the virtual environment: `source venv/bin/activate`
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`

### Technology Stack

* Django 3.2
* Django REST framework 3.12
* Python 3.9
* SQLite database

## Test Suite

The test suite is located in the `tests` directory. You can run the tests using the following command:
1. `python manage.py test`

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Authors
* Saurabh Patil

## Acknowledgments
* Django REST framework for providing a robust API framework
* Python for being an awesome programming language
