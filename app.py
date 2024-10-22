from flask import Flask
from config import Config
from ex import db, bcrypt  # Import db and bcrypt from extensions
from routes import costumer_bp, order_bp, product_bp

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from the Config class

    # Initialize the database and bcrypt with the app
    db.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints for different routes
    app.register_blueprint(costumer_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(product_bp)

    return app

if __name__ == '__main__':
    app = create_app()  # Create the Flask application instance
    with app.app_context():
        db.create_all()
    app.run(debug=True)
