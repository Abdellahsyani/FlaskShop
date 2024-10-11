from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .product import Product
from .order import Order
from .product_order import ProductOrder
from .costumer import Costumer
