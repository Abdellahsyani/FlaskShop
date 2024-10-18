from ex import db


class Product(db.Model):
    """Product model to hold product information."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

    orders = db.relationship('ProductOrder', back_populates='product', cascade="all, delete-orphan")

    def __init__(self, name, price):
        self.name = name
        self.price = price
