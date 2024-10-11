from flask import Flask
from  models import db
from routes import product_bp
from routes import order_bp

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)

    return app

# Create an app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
