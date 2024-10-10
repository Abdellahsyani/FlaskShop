@order_bp.route('/orders', methods=['POST'])
def create_order():
    """Define the order endpoint for POST requests."""
    data = request.get_json()
    user_id = data.get('user_id')  # Keep it as it is
    products = data.get('products')  # List of product IDs with quantities

    if not user_id or not products:
        return jsonify({'error': 'Missing user_id or products'}), 400

    # Create a new order
    order = Order(costumer_id=user_id)  # Correct attribute name
    db.session.add(order)

    for product_data in products:
        product_id = product_data.get('product_id')
        quantity = product_data.get('quantity')

        # Check if the product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': f'Product with ID {product_id} does not exist'}), 404

        # Create a ProductOrder entry
        order_product = ProductOrder(order_id=order.id, product_id=product_id, quantity=quantity)
        db.session.add(order_product)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500  # Handle any commit errors

    return jsonify({'message': 'Order created successfully', 'order_id': order.id}), 201
