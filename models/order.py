from ex import db


class Order(db.Model):
    """Start order class to collect the product of the customer."""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    costumer_id = db.Column(db.Integer, db.ForeignKey('costumers.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    products = db.relationship('ProductOrder', back_populates='order', cascade="all, delete-orphan")

    def __init__(self, costumer_id, product_id, quantity):
        self.costumer_id = costumer_id
        self.product_id = product_id
        self.quantity = quantity
