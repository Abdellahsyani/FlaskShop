from flask import Blueprint, request, jsonify
from models.order import Order
from models.product_order import ProductOrder
from models.product import Product
from ex import db

bp = Blueprint('order_routes', __name__)

@bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data['costumer_id']
    product_id = data['product_id']
    quantity = data['quantity']

    # Create a new order
    new_order = Order(costumer_id=user_id, product_id=product_id, quantity=quantity)
    db.session.add(new_order)
    db.session.commit()

    # Link the order with a product
    product = Product.query.get(product_id)
    if product:
        product_order = ProductOrder(order_id=new_order.id, product_id=product_id, quantity=quantity)
        db.session.add(product_order)
        db.session.commit()
        return jsonify({"message": "Order created successfully."}), 201

    return jsonify({"message": "Product not found."}), 404

@bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{"id": order.id, "product_id": order.product_id, "costumer_id": order.costumer_id, "quantity": order.quantity} for order in orders]), 200

@bp.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    if order:
        return jsonify({"id": order.id, "product_id": order.product_id, "costumer_id": order.costumer_id, "quantity": order.quantity}), 200
    return jsonify({"message": "Order not found."}), 404

@bp.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"message": "Order not found."}), 404

    data = request.get_json()
    order.costumer_id = data.get('costumer_id', order.costumer_id)
    
    db.session.commit()
    return jsonify({"message": "Order updated successfully."}), 200

@bp.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"message": "Order not found."}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully."}), 200
