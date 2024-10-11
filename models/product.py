from models import db

class Product(db.Model):
    """create a table for product listing"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)

    orders = db.relationship('ProductOrder', back_populates='product', cascade='all, delete-orphan', single_parent=True)
