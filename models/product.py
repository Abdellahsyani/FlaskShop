from ex import db


class Product(db.Model):
    """Represents a product in the store, holding essential product details."""

    __tablename__ = 'products'

    # Primary key for the products table
    id = db.Column(db.Integer, primary_key=True)

    # Name of the product with a maximum length of 200 characters
    name = db.Column(db.String(200), nullable=False)

    # Price of the product, represented as a floating-point number
    price = db.Column(db.Float, nullable=False)

    # Relationship to ProductOrder, enabling backreference and cascading delete
    orders = db.relationship('ProductOrder', back_populates='product', cascade="all, delete-orphan")


    def __init__(self, name, price):
        """
        Initializes a Product instance.

        :param name: Name of the product
        :param price: Price of the product
        """
        self.name = name
        self.price = price
