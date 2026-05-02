from .customer_routes import bp as costumer_bp
from .order_routes import bp as order_bp
from .product_routes import bp as product_bp
from .frontend_routes import bp as frontend_bp

__all__ = ['costumer_bp', 'order_bp', 'product_bp', 'frontend_bp']
