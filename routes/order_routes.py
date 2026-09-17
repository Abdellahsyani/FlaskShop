from flask import Blueprint, request, jsonify
from models.order import Order
from models.product_order import ProductOrder
from models.product import Product
from ex import db

bp = Blueprint('order_routes', __name__)

REQUIRED_FIELDS = ('costumer_id', 'product_id', 'quantity')


def serialize_order(order):
    product = Product.query.get(order.product_id)
    return {
        "id": order.id,
        "product_id": order.product_id,
        "product_name": product.name if product else None,
        "costumer_id": order.costumer_id,
        "quantity": order.quantity,
    }


@bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "Request body must be JSON."}), 400
    missing = [field for field in REQUIRED_FIELDS if data.get(field) is None]
    if missing:
        return jsonify({"message": f"Missing required fields: {', '.join(missing)}."}), 400

    product_id = data['product_id']
    quantity = data['quantity']

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found."}), 404

    new_order = Order(costumer_id=data['costumer_id'], product_id=product_id, quantity=quantity)
    db.session.add(new_order)
    db.session.commit()

    product_order = ProductOrder(order_id=new_order.id, product_id=product_id, quantity=quantity)
    db.session.add(product_order)
    db.session.commit()

    return jsonify({"id": new_order.id, "message": "Order created successfully."}), 201

@bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([serialize_order(order) for order in orders]), 200

@bp.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    if order:
        return jsonify(serialize_order(order)), 200
    return jsonify({"message": "Order not found."}), 404

@bp.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"message": "Order not found."}), 404

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message": "Request body must be JSON."}), 400
    order.costumer_id = data.get('costumer_id', order.costumer_id)
    order.quantity = data.get('quantity', order.quantity)
    
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
