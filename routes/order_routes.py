from flask import Blueprint, request, jsonify
from models import db, Order, Product, ProductOrder

order_bp = Blueprint('orders', __name__)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    """Define the order endpoint for POST requests."""
    data = request.get_json()
    user_id = data.get('user_id')
    products = data.get('products')

    if not user_id or not products:
        return jsonify({'error': 'Missing user_id or products'}), 400

    order = Order(costumer_id=user_id)
    db.session.add(order)

    for product_data in products:
        product_id = product_data.get('product_id')
        quantity = product_data.get('quantity')

        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': f'Product with ID {product_id} does not exist'}), 404

        order_product = ProductOrder(order_id=order.id, product_id=product_id, quantity=quantity)
        db.session.add(order_product)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Order created successfully', 'order_id': order.id}), 201
