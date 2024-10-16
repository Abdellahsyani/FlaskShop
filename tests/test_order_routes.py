import unittest
from flask import Flask
from ex import db
from routes.order_routes import bp as order_routes
from models.order import Order
from models.product import Product
from models.costomer import Costomer
from models.product_order import ProductOrder

class OrderRoutesTest(unittest.TestCase):

    def setUp(self):
        # Create a new Flask application for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
        db.init_app(self.app)  # Initialize the db with the app
        self.app.register_blueprint(order_routes)

        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()  # Create the database tables

            # Optional: Set up initial data for your tests
            # Example of creating a product and customer
            self.customer = Customer(first_name='John', last_name='Doe')
            self.product = Product(name='Test Product', price=100)
            db.session.add(self.customer)
            db.session.add(self.product)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()  # Clean up the database after each test

    def test_create_order(self):
        response = self.client.post('/orders', json={
            'costumer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Order created successfully.', response.data)

    def test_get_orders(self):
        # Create an order first
        self.client.post('/orders', json={
            'costumer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 2
        })

        response = self.client.get('/orders')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)  # Should return a list of orders

    def test_get_order(self):
        response = self.client.post('/orders', json={
            'costumer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 2
        })
        order_id = response.json['id']

        response = self.client.get(f'/orders/{order_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['costumer_id'], self.customer.id)

    def test_update_order(self):
        response = self.client.post('/orders', json={
            'costumer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 2
        })
        order_id = response.json['id']

        response = self.client.put(f'/orders/{order_id}', json={
            'costumer_id': 2  # Assuming you want to change the customer id
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Order updated successfully.', response.data)

    def test_delete_order(self):
        response = self.client.post('/orders', json={
            'costumer_id': self.customer.id,
            'product_id': self.product.id,
            'quantity': 2
        })
        order_id = response.json['id']

        response = self.client.delete(f'/orders/{order_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Order deleted successfully.', response.data)

        # Verify the order is actually deleted
        response = self.client.get(f'/orders/{order_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Order not found.', response.data)

if __name__ == '__main__':
    unittest.main()
