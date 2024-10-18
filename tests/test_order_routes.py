import unittest
from flask import json
from app import create_app, db
from models.costumer import Costumer
from models.product import Product
from models.order import Order

class OrderRoutesTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()  # Call without arguments to use the default config
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()  # Create the database tables

        # Create test data
        self.costumer = Costumer(email='john.doe@example.com', password='password', first_name='John', last_name='Doe')
        self.product = Product(name='Test Product', price=10.00)
        db.session.add(self.costumer)
        db.session.add(self.product)
        db.session.commit()

        self.order_data = {
            'costumer_id': self.costumer.id,
            'product_id': self.product.id,
            'quantity': 2
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_order(self):
        response = self.app.test_client().post('/orders', json=self.order_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Order created successfully.', response.data)

    def test_get_orders(self):
        self.app.test_client().post('/orders', json=self.order_data)
        response = self.app.test_client().get('/orders')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertGreater(len(response_data), 0)
        self.assertEqual(response_data[0]['costumer_id'], self.costumer.id)
        self.assertEqual(response_data[0]['product_id'], self.product.id)
        self.assertEqual(response_data[0]['quantity'], self.order_data['quantity'])

    def test_get_order(self):
        response = self.app.test_client().post('/orders', json=self.order_data)
        order_id = json.loads(response.data)['id']
        response = self.app.test_client().get(f'/orders/{order_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product', response.data)

    def test_update_order(self):
        response = self.app.test_client().post('/orders', json=self.order_data)
        self.assertEqual(response.status_code, 201)

        try:
            order_id = json.loads(response.data)['id']
        except KeyError:
            print("Response data:", response.data)
            self.fail("Response does not contain 'id' key")
        updated_data = {'costumer_id': self.costumer.id}
        response = self.app.test_client().put(f'/orders/{order_id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Order updated successfully.', response.data)

    def test_delete_order(self):
        response = self.app.test_client().post('/orders', json=self.order_data)
        order_id = json.loads(response.data)['id']
        response = self.app.test_client().delete(f'/orders/{order_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Order deleted successfully.', response.data)

if __name__ == '__main__':
    unittest.main()

