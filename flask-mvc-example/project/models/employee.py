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


def findAllEmployees():
    with _get_connection().session() as session:
        employee = session.run("MATCH (a:Employee) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in employee]
        print(nodes_json)
        return nodes_json


def save_employee(name, address, branch):
    with _get_connection().session() as session:
        employee = session.run("MERGE (a:Employee{name: $name, address: $address, branch: $branch}) RETURN a;", name = name, address = address, branch = branch)
        nodes_json = [node_to_json(record["a"]) for record in employee]
        print(nodes_json)
        return nodes_json

def update_employee(name, address, branch):
    with _get_connection().session() as session:
        employee = session.run("MATCH (a:Employee{name:$name}) set a.address=$address, a.branch=$branch RETURN a;", name = name, address = address, branch = branch)
        print(employee)
        nodes_json = [node_to_json(record["a"]) for record in employee]
        print(nodes_json)
        return nodes_json

def delete_employee(name):
    _get_connection().execute_query("MATCH (a:Employee{name: $name}) delete a;", name =name)