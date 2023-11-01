from project import app
from flask import render_template, request, redirect, url_for
from project.models.User import findUserByUsername
from project.models.getcars import *
from project.models.customer import save_customer, delete_customer, update_customer, findAllCustomers
from project.models.employee import findAllEmployees, save_employee, update_employee, delete_employee

#route index
@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        username = request.form["username"]
        try:
            user = findUserByUsername(username)
            data = {
                "username": user.username,
                "email": user.email
            }
        except Exception as err:
            print (err)

    else:
        data = {
            "username": "Not specified",
            "email": "Not specified"
        }
    return render_template('index.html.j2', data = data)

# Cars:

@app.route('/get_cars', methods=['GET'])
def query_records_cars():
    return findAllCars()

@app.route('/save_car', methods=["POST"])
def save_car_info():
    record = json.loads(request.data)
    print(record)
    return save_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])

@app.route('/update_car', methods=['PUT'])
def update_car_info():
    record = json.loads(request.data)
    print(record)
    return update_car(record['make'], record['model'], record['reg'], record['year'], record['capacity'])

@app.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    record = json.loads(request.data)
    print(record)
    delete_car(record['reg'])
    return findAllCars()

@app.route('/order-car', methods=['POST'])
def order_car_endpoint():
    try:
        data = request.json
        customer_id = data['customer_id']
        car_id = data['car_id']
        result = order_car(customer_id, car_id)  # This function should be imported from getcars.py
        return jsonify(result), 200 if result['status'] == 'success' else 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

#Customer
@app.route('/get_customers', methods=['GET'])
def query_records_customer():
    return findAllCustomers()

@app.route('/save_customer', methods=["POST"])
def save_customer_info():
    record = json.loads(request.data)
    print(record)
    return save_customer(record['name'], record['age'], record['address'])

@app.route('/update_customer', methods=['PUT'])
def update_customer_info():
    record = json.loads(request.data)
    print(record)
    return update_customer(record['name'], record['age'], record['address'])

@app.route('/delete_customer', methods=['DELETE'])
def delete_customer_info():
    record = json.loads(request.data)
    print(record)
    delete_customer(record['name'])
    return findAllCustomers()

#Employee
@app.route('/get_employees', methods=['GET'])
def query_records_employee():
    return findAllEmployees()

@app.route('/save_employee', methods=["POST"])
def save_employee_info():
    record = json.loads(request.data)
    print(record)
    return save_employee(record['name'], record['address'], record['branch'])

@app.route('/update_employee', methods=['PUT'])
def update_employee_info():
    record = json.loads(request.data)
    print(record)
    return update_employee(record['name'], record['address'], record['branch'])

@app.route('/delete_employee', methods=['DELETE'])
def delete_employee_info():
    record = json.loads(request.data)
    print(record)
    delete_employee(record['name'])
    return findAllEmployees()

@app.route('/cancel-order-car', methods=['POST'])
def cancel_order_endpoint():
    try:
        data = request.json
        customer_id = data['customer_id']
        car_id = data['car_id']
        result = cancel_order(customer_id, car_id)
        return jsonify(result), 200 if result['status'] == 'success' else 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/rent-car', methods=['POST'])
def rent_car_endpoint():
    try:
        data = request.json
        customer_id = data['customer_id']
        car_id = data['car_id']
        result = rent_car(customer_id, car_id)
        return jsonify(result), 200 if result['status'] == 'success' else 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/return-car', methods=['POST'])
def return_car_endpoint():
    try:
        data = request.json
        customer_id = data['customer_id']
        car_id = data['car_id']
        car_status = data['car_status']  # This should be either 'ok' or 'damaged'
        result = return_car(customer_id, car_id, car_status)
        return jsonify(result), 200 if result['status'] == 'success' else 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500