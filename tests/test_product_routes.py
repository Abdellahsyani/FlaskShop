import unittest
from flask import Flask
from ex import db
from routes.product_routes import bp as product_routes
from models.product import Product

class ProductRoutesTest(unittest.TestCase):

    def setUp(self):
        # Create a new Flask application for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
        db.init_app(self.app)  # Initialize the db with the app
        self.app.register_blueprint(product_routes)

        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()  # Create the database tables

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()  # Clean up the database after each test

    def test_create_product(self):
        response = self.client.post('/products', json={
            'name': 'Test Product',
            'price': 100
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Product created successfully.', response.data)

    def test_get_products(self):
        # First, add a product to the database
        with self.app.app_context():
            product = Product(name='Test Product', price=100)
            db.session.add(product)
            db.session.commit()

        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product', response.data)

    def test_get_product(self):
        # Add a product to the database
        with self.app.app_context():
            product = Product(name='Test Product', price=100)
            db.session.add(product)
            db.session.commit()

        response = self.client.get('/products/1')  # Assuming the product ID is 1
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product', response.data)

    def test_get_product_not_found(self):
        response = self.client.get('/products/999')  # Non-existent product ID
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Product not found.', response.data)

    def test_update_product(self):
        # Add a product to the database
        with self.app.app_context():
            product = Product(name='Test Product', price=100)
            db.session.add(product)
            db.session.commit()

        response = self.client.put('/products/1', json={
            'name': 'Updated Product',
            'price': 150
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product updated successfully.', response.data)

        # Check if the product was updated
        response = self.client.get('/products/1')
        self.assertIn(b'Updated Product', response.data)

    def test_update_product_not_found(self):
        response = self.client.put('/products/999', json={
            'name': 'Updated Product',
            'price': 150
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Product not found.', response.data)

    def test_delete_product(self):
        # Add a product to the database
        with self.app.app_context():
            product = Product(name='Test Product', price=100)
            db.session.add(product)
            db.session.commit()

        response = self.client.delete('/products/1')  # Assuming the product ID is 1
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product deleted successfully.', response.data)

        # Check if the product was deleted
        response = self.client.get('/products/1')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Product not found.', response.data)

    def test_delete_product_not_found(self):
        response = self.client.delete('/products/999')  # Non-existent product ID
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Product not found.', response.data)

if __name__ == '__main__':
    unittest.main()
