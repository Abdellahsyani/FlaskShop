from flask import Flask
from  models.db import db
from routes import product_bp
from routes import order_bp

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)  # Correct usage to initialize the db with the app

    # Register blueprints (your routes)
    app.register_blueprint(product_bp)

    return app

# Create an app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)  # You can specify host and port if needed
