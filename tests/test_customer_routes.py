import unittest
from app import create_app
from ex import db
from models import Costumer

class CustomerRoutesTest(unittest.TestCase):

    def setUp(self):
        """Set up a test client and a fresh database before each test."""
        self.app = create_app()  # No arguments passed here
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()  # Create all tables

    def tearDown(self):
        """Clean up the database after each test."""
        with self.app.app_context():
            db.session.remove()  # Remove the session
            db.drop_all()  # Drop all tables

    def test_create_customer(self):
        response = self.client.post('/customers', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Customer created successfully.', response.get_data(as_text=True))

    def test_get_customers(self):
        with self.app.app_context():
            customer = Costumer(first_name='John', last_name='Doe', email='johndoe@example.com', password='password123')
            db.session.add(customer)
            db.session.commit()

        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertIn('John', response.get_data(as_text=True))

    def test_get_customer(self):
        with self.app.app_context():
            customer = Costumer(first_name='John', last_name='Doe', email='johndoe@example.com', password='password123')
            db.session.add(customer)
            db.session.commit()
            customer_id = customer.id

        response = self.client.get(f'/customers/{customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('John', response.get_data(as_text=True))

    def test_update_customer(self):
        # Add a customer to the database
        with self.app.app_context():
            customer = Costumer(first_name='John', last_name='Doe', email='johndoe@example.com', password='password123')
            db.session.add(customer)
            db.session.commit()

            # Store the customer ID before the session ends
            customer_id = customer.id

            # Test updating the customer
            response = self.client.put(f'/customers/{customer_id}', json={'first_name': 'Jane'})
            self.assertEqual(response.status_code, 200)
            self.assertIn('Customer updated successfully.', response.get_data(as_text=True))

            # Reload the customer after the PUT request to verify updates
            updated_customer = Costumer.query.get(customer_id)
            self.assertEqual(updated_customer.first_name, 'Jane')

    def test_delete_customer(self):
        with self.app.app_context():
            customer = Costumer(first_name='John', last_name='Doe', email='johndoe@example.com', password='password123')
            db.session.add(customer)
            db.session.commit()
            customer_id = customer.id

        response = self.client.delete(f'/customers/{customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Customer deleted successfully.', response.get_data(as_text=True))

        # Verify that the customer is deleted
        response = self.client.get(f'/customers/{customer_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Customer not found.', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
