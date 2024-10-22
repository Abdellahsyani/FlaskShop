from ex import db


class ProductOrder(db.Model):
    """Create the join table to implement many-to-many in product and order tables."""

    __tablename__ = 'productorders'

    # Foreign key referencing the order ID, part of the composite primary key
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)

    # Foreign key referencing the product ID, part of the composite primary key
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete="CASCADE"), primary_key=True)

    # Quantity of the product in the order
    quantity = db.Column(db.Integer, nullable=False)

    # Relationship to the Product model, enabling backreference
    product = db.relationship('Product', back_populates='orders')

    # Relationship to the Order model, enabling backreference
    order = db.relationship('Order', back_populates='products')
