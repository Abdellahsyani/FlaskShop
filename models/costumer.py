from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class Costumer(db.Model):
    """the costumer table that hold all the info about costumer
    """
    __tablename__ = 'costumers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(155), unique=True)
    last_name = db.Column(db.String(155), unique=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, email, password):
        """hashing the password before store int in db
        """
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """checking the password
        """
        return bcrypt.check_password_hash(self.password, password)
