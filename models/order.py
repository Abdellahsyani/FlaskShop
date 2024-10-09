from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Orders(db.Model):
    """start order class to collect the product of the costumer
    """
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    costumer_id = db.Column(db.Integer, db.Foreignkey('costumers.id'), nullable=False)

    products = db.ralationship('ProductOrder', back_populates='order')
