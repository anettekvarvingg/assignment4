
from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json
URI = "neo4j+s://2507e467.databases.neo4j.io"
AUTH = ("neo4j", "SFlXJba3T94_6ImZ6Uwgh4OYEo_O5_XAxFEmYNFLtHE")
def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver
def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties


def findAllCars():
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json


def save_car(make, model, reg, year, capacity):
    with _get_connection().session() as session:
        cars = session.run("MERGE (a:Car{make: $make, model: $model, reg: $reg, year: $year, capacity:$capacity}) RETURN a;", make = make, model = model, reg = reg, year =year, capacity = capacity)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json


def update_car(make, model, reg, year, capacity):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car{reg:$reg}) set a.make=$make, a.model=$model, a.year = $year, a.capacity = $capacity RETURN a;", reg=reg, make=make, model=model, year=year, capacity=capacity)
        print(cars)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

def delete_car(reg):
    _get_connection().execute_query("MATCH (a:Car{reg: $reg}) delete a;", reg =reg)

#Order car:
def order_car(customer_id, car_id):
    with _get_connection().session() as session:
        customer_check = session.run("MATCH (c:Customer)-[:BOOKED|:RENTED]->(a:Car) WHERE c.id = $customer_id RETURN a", customer_id=customer_id)
        if customer_check.single():
            return {"status": "error", "message": "Customer has already booked or rented another car."}
        car_check = session.run("MATCH (a:Car) WHERE a.id = $car_id AND a.status = 'available' RETURN a", car_id=car_id)
        if not car_check.single():
            return {"status": "error", "message": "Car is not available."}
        session.run("MATCH (c:Customer), (a:Car) WHERE c.id = $customer_id AND a.id = $car_id MERGE (c)-[:BOOKED]->(a) SET a.status = 'booked'", customer_id=customer_id, car_id=car_id)
        return {"status": "success", "message": "Car booked successfully."}

#Cancel order:
def cancel_order(customer_id, car_id):
    with _get_connection().session() as session:
        customer_check = session.run("MATCH (c:Customer)-[r:BOOKED]->(a:Car) WHERE c.id = $customer_id AND a.id = $car_id RETURN r", customer_id=customer_id, car_id=car_id)
        if not customer_check.single():
            return {"status": "error", "message": "Customer has not booked the specified car."}
        session.run("MATCH (c:Customer)-[r:BOOKED]->(a:Car) WHERE c.id = $customer_id AND a.id = $car_id DELETE r SET a.status = 'available'", customer_id=customer_id, car_id=car_id)

        return {"status": "success", "message": "Car booking cancelled successfully."}

#Rent order:
def rent_car(customer_id, car_id):
    with _get_connection().session() as session:
        customer_check = session.run("MATCH (c:Customer)-[r:BOOKED]->(a:Car) WHERE c.id = $customer_id AND a.id = $car_id RETURN r", customer_id=customer_id, car_id=car_id)
        if not customer_check.single():
            return {"status": "error", "message": "Customer has not booked the specified car."}
        session.run("MATCH (c:Customer)-[r:BOOKED]->(a:Car) WHERE c.id = $customer_id AND a.id = $car_id DELETE r CREATE (c)-[:RENTED]->(a) SET a.status = 'rented'", customer_id=customer_id, car_id=car_id)

        return {"status": "success", "message": "Car rented successfully."}

#Return car:
def return_car(customer_id, car_id, car_status):
    with _get_connection().session() as session:
        customer_check = session.run("MATCH (c:Customer)-[r:RENTED]->(a:Car) WHERE c.id = $customer_id AND a.id = $car_id RETURN r", customer_id=customer_id, car_id=car_id)
        if not customer_check.single():
            return {"status": "error", "message": "Customer has not rented the specified car."}
        new_status = 'available' if car_status == 'ok' else 'damaged'
        session.run("MATCH (c:Customer)-[r:RENTED]->(a:Car) WHERE c.id = $customer_id AND a.id = $car_id DELETE r SET a.status = $new_status", customer_id=customer_id, car_id=car_id, new_status=new_status)

        return {"status": "success", "message": "Car returned successfully."}
