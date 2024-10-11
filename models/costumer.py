from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Costumer(db.Model):
    """The customer table that holds all the info about customers."""
    __tablename__ = 'costumers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(155), unique=True)
    last_name = db.Column(db.String(155), unique=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, email, password):
        """Hash the password before storing it in the database."""
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if the hashed password matches."""
        return bcrypt.check_password_hash(self.password, password)
