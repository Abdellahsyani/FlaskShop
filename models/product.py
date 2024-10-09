from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class product(db.Model):
    """create a table for product listining
    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)

    orders = db.relationship('ProductOrder', back_populates='product')
