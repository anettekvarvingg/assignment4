
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


def findAllCustomers():
    with _get_connection().session() as session:
        customer = session.run("MATCH (a:Customer) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in customer]
        print(nodes_json)
        return nodes_json

def save_customer(name, age, address):
    try:
        with _get_connection().session() as session:
            customer = session.run("MERGE (a:Customer{name: $name, age: $age, address: $address}) RETURN a;", name = name, age = age, address = address)
            nodes_json = [node_to_json(record["a"]) for record in customer]
            print(nodes_json)
            return nodes_json
    except Exception as r:
        print(r)

def update_customer(name, age, address):
    with _get_connection().session() as session:
        customer = session.run("MATCH (a:Customer{name:$name}) set a.age=$age, a.address=$address RETURN a;", name = name, age = age, address = address)
        print(customer)
        nodes_json = [node_to_json(record["a"]) for record in customer]
        print(nodes_json)
        return nodes_json

def delete_customer(name):
    _get_connection().execute_query("MATCH (a:Customer{name: $name}) delete a;", name =name)