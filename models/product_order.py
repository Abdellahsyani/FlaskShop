from .db import db

class ProductOrder(db.Model):
    """create the join table to implement many-to-many in product and order tables"""
    __tablename__ = 'productorders'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', back_populates='orders')
    order = db.relationship('Order', back_populates='products')
