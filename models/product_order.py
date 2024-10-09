from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ProductOrder(db.Model):
    """create the join table to implement many to many in product and order tables
    """
    __tablename__ = 'productorders'

    order_id = db.Column(db.Integer, db.Foreignkey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.Foreignkey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', back_populates='products')
    product = db.ralationship('Product', back_populates='orders')
