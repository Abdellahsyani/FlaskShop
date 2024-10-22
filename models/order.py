from ex import db


class Order(db.Model):
    """Start order class to collect the product of the customer."""
    __tablename__ = 'orders'

    # Primary key for the orders table
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key linking to the products table
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    # Foreign key linking to the customers table (note the typo in 'costumer', which should be 'costumer')
    costumer_id = db.Column(db.Integer, db.ForeignKey('costumers.id'), nullable=False)

    # Number of items of the product in the order
    quantity = db.Column(db.Integer, nullable=False)

    # Relationship to ProductOrder, enabling backreference and cascading delete
    products = db.relationship('ProductOrder', back_populates='order', cascade="all, delete-orphan")

    def __init__(self, costumer_id, product_id, quantity):
        """
        Initialize an Order instance.
        :param costumer_id: ID of the costumer placing the order
        :param product_id: ID of the product being ordered
        :param quantity: Quantity of the product in the order
        """
        self.costumer_id = costumer_id
        self.product_id = product_id
        self.quantity = quantity
