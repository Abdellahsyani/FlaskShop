from flask import Blueprint, request, jsonify
from models.product import Product
from ex import db

bp = Blueprint('product_routes', __name__)

@bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully."}), 201

@bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": product.id, "name": product.name, "price": product.price} for product in products]), 200

@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify({"id": product.id, "name": product.name, "price": product.price}), 200
    return jsonify({"message": "Product not found."}), 404

@bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found."}), 404

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)

    db.session.commit()
    return jsonify({"message": "Product updated successfully."}), 200

@bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found."}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully."}), 200
