from flask import Blueprint, request, jsonify
from models import Costumer
from ex import db

bp = Blueprint('customer_routes', __name__)

@bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Costumer(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer created successfully."}), 201

@bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Costumer.query.all()
    return jsonify([{"id": customer.id, "first_name": customer.first_name, "last_name": customer.last_name, "email": customer.email} for customer in customers]), 200

@bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Costumer.query.get(id)
    if customer:
        return jsonify({"id": customer.id, "first_name": customer.first_name, "last_name": customer.last_name, "email": customer.email}), 200
    return jsonify({"message": "Customer not found."}), 404

@bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Costumer.query.get(id)
    if not customer:
        return jsonify({"message": "Customer not found."}), 404
    
    data = request.get_json()
    customer.first_name = data.get('first_name', customer.first_name)
    customer.last_name = data.get('last_name', customer.last_name)
    customer.email = data.get('email', customer.email)
    if 'password' in data:
        customer.password = data['password']

    db.session.commit()
    return jsonify({"message": "Customer updated successfully."}), 200

@bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Costumer.query.get(id)
    if not customer:
        return jsonify({"message": "Customer not found."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully."}), 200
