from flask import Blueprint, request, jsonify
from models import db, Product, ProductOrder

product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['POST'])
def create_product():
    """Define the product endpoint for POST requests."""
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    if not name or not price:
        return jsonify({'error': 'Missing name or price'}), 400

    product = Product(name=name, price=price)
    db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully', 
                    'product': {'id': product.id, 'name': product.name, 'price': product.price}}), 201

@product_bp.route('/products', methods=['GET'])
def get_products():
    """Define the product endpoint for GET requests."""
    products = Product.query.all()
    product_list = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]

    return jsonify(product_list), 200
