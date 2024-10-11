from flask_sqlalchemy import SQLAlchemy
from ex import db


class Order(db.Model):
    """Start order class to collect the product of the customer."""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    costumer_id = db.Column(db.Integer, db.ForeignKey('costumers.id'), nullable=False)

    products = db.relationship('ProductOrder', back_populates='order')

    def __init__(self, costumer_id):
        self.costumer_id = costumer_id
