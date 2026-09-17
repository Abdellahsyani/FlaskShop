# FlaskShop

A small e-commerce backend built with Flask. It exposes a JSON REST API for
managing **customers**, **products** and **orders**, and serves a
server-rendered **admin UI** (vanilla JavaScript) at `/` for interacting with
that API from the browser. Data is persisted with SQLAlchemy in a SQLite
database.

## Features

- **Application factory** – `create_app()` in `app.py` builds and configures
  the Flask app and registers all blueprints.
- **Blueprint routing** – each resource lives in its own blueprint under
  `routes/` (`customer_routes.py`, `product_routes.py`, `order_routes.py`,
  `frontend_routes.py`).
- **SQLAlchemy models** – `models/` defines the `Costumer`, `Product`, `Order`
  and `ProductOrder` tables via Flask-SQLAlchemy.
- **Bcrypt password hashing** – customer passwords are hashed with
  Flask-Bcrypt in `models/costumer.py` before being stored.
- **SQLite storage** – `config.py` points SQLAlchemy at a SQLite database by
  default (configurable via `DATABASE_URL`).
- **Admin frontend** – `templates/index.html` plus `static/app.js` and
  `static/styles.css` provide a simple UI to create/list customers, products
  and orders.
- **Test suite** – `unittest`-based integration tests for every route in
  `tests/`.

## Project structure

```
FlaskShop/
├── app.py                  # create_app() factory + dev entrypoint
├── config.py               # Config class (DATABASE_URL, SQLAlchemy settings)
├── ex.py                   # Shared extension instances: db (SQLAlchemy), bcrypt
├── requirements.txt        # Python dependencies
├── AUTHORS
├── models/
│   ├── __init__.py
│   ├── costumer.py         # Costumer model (table: costumers)
│   ├── product.py          # Product model (table: products)
│   ├── order.py            # Order model (table: orders)
│   └── product_order.py    # ProductOrder join model (table: productorders)
├── routes/
│   ├── __init__.py
│   ├── customer_routes.py  # /customers endpoints
│   ├── product_routes.py   # /products endpoints
│   ├── order_routes.py     # /orders endpoints
│   └── frontend_routes.py  # GET / (admin UI)
├── static/
│   ├── app.js
│   └── styles.css
├── templates/
│   └── index.html
└── tests/
    ├── test_customer_routes.py
    ├── test_product_routes.py
    └── test_order_routes.py
```

## Requirements

- Python 3.x
- `pip`

All Python dependencies are listed in `requirements.txt`:

| Package            | Import used in code                          |
| ------------------ | -------------------------------------------- |
| `Flask`            | `from flask import ...`                      |
| `Flask-SQLAlchemy` | `from flask_sqlalchemy import SQLAlchemy`    |
| `Flask-Bcrypt`     | `from flask_bcrypt import Bcrypt`            |

## Installation

```bash
git clone https://github.com/Abdellahsyani/FlaskShop.git
cd FlaskShop

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Configuration

Configuration lives in `config.py`:

| Setting                          | Source / default                              | Description                                                                 |
| -------------------------------- | --------------------------------------------- | --------------------------------------------------------------------------- |
| `SQLALCHEMY_DATABASE_URI`        | `DATABASE_URL` env var, default `sqlite:///shop.db` | Database connection string. With the default, Flask creates `instance/shop.db`. |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | `False`                                       | Disables SQLAlchemy's modification-tracking signals to save memory.        |

Example of pointing the app at another database:

```bash
export DATABASE_URL="sqlite:////tmp/flaskshop.db"
```

## Running the app

```bash
python app.py
```

On startup the app calls `db.create_all()` to create any missing tables, then
starts the development server (with `debug=True`) at
**http://127.0.0.1:5000/**.

- `GET /` serves the admin UI (`templates/index.html`).
- All other endpoints below accept and return JSON.

## API reference

All request bodies are JSON (`Content-Type: application/json`). Every
"not found" response has the shape `{"message": "<Resource> not found."}`.

> **Note:** the customer foreign key on orders is spelled `costumer_id`
> (matching the `costumers` table name in the code). Use that exact spelling
> in request bodies.

### Customers (`routes/customer_routes.py`)

| Method   | Path               | Request body                                              | Success response                                                        | Errors |
| -------- | ------------------ | --------------------------------------------------------- | ----------------------------------------------------------------------- | ------ |
| `POST`   | `/customers`       | `first_name`, `last_name`, `email`, `password` (all required) | `201` `{"message": "Customer created successfully."}`                | –      |
| `GET`    | `/customers`       | –                                                         | `200` `[{"id", "first_name", "last_name", "email"}, ...]`               | –      |
| `GET`    | `/customers/<id>`  | –                                                         | `200` `{"id", "first_name", "last_name", "email"}`                      | `404`  |
| `PUT`    | `/customers/<id>`  | Any of `first_name`, `last_name`, `email`, `password` (partial update) | `200` `{"message": "Customer updated successfully."}`      | `404`  |
| `DELETE` | `/customers/<id>`  | –                                                         | `200` `{"message": "Customer deleted successfully."}`                   | `404`  |

Passwords are hashed with bcrypt on creation and are never returned by the API.

### Products (`routes/product_routes.py`)

| Method   | Path              | Request body                                | Success response                                       | Errors |
| -------- | ----------------- | ------------------------------------------- | ------------------------------------------------------ | ------ |
| `POST`   | `/products`       | `name` (string), `price` (number) – required | `201` `{"message": "Product created successfully."}`  | –      |
| `GET`    | `/products`       | –                                           | `200` `[{"id", "name", "price"}, ...]`                 | –      |
| `GET`    | `/products/<id>`  | –                                           | `200` `{"id", "name", "price"}`                        | `404`  |
| `PUT`    | `/products/<id>`  | Any of `name`, `price` (partial update)     | `200` `{"message": "Product updated successfully."}`   | `404`  |
| `DELETE` | `/products/<id>`  | –                                           | `200` `{"message": "Product deleted successfully."}`   | `404`  |

### Orders (`routes/order_routes.py`)

| Method   | Path            | Request body                                                  | Success response                                              | Errors |
| -------- | --------------- | ------------------------------------------------------------- | ------------------------------------------------------------- | ------ |
| `POST`   | `/orders`       | `costumer_id` (int), `product_id` (int), `quantity` (int) – required | `201` `{"message": "Order created successfully."}`     | `404` if the product does not exist |
| `GET`    | `/orders`       | –                                                             | `200` `[{"id", "product_id", "costumer_id", "quantity"}, ...]` | –      |
| `GET`    | `/orders/<id>`  | –                                                             | `200` `{"id", "product_id", "costumer_id", "quantity"}`       | `404`  |
| `PUT`    | `/orders/<id>`  | Any of `costumer_id`, `quantity` (partial update)             | `200` `{"message": "Order updated successfully."}`            | `404`  |
| `DELETE` | `/orders/<id>`  | –                                                             | `200` `{"message": "Order deleted successfully."}`            | `404`  |

Creating an order inserts a row in `orders` and, if the product exists, a
matching row in the `productorders` join table.

There is currently **no authentication or login endpoint**; all routes are
open.

### Example `curl` requests

Create a customer:

```bash
curl -X POST http://127.0.0.1:5000/customers \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jane", "last_name": "Doe", "email": "jane@example.com", "password": "s3cret"}'
```

Create a product:

```bash
curl -X POST http://127.0.0.1:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Keyboard", "price": 49.99}'
```

Create an order (note `costumer_id`):

```bash
curl -X POST http://127.0.0.1:5000/orders \
  -H "Content-Type: application/json" \
  -d '{"costumer_id": 1, "product_id": 1, "quantity": 2}'
```

List and fetch:

```bash
curl http://127.0.0.1:5000/customers
curl http://127.0.0.1:5000/products/1
curl http://127.0.0.1:5000/orders/1
```

Update and delete:

```bash
curl -X PUT http://127.0.0.1:5000/products/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 39.99}'

curl -X DELETE http://127.0.0.1:5000/orders/1
```

## Data model

Defined in `models/` using the shared `db` instance from `ex.py`.

### `costumers` (`models/costumer.py` – `Costumer`)

| Column       | Type          | Constraints                |
| ------------ | ------------- | -------------------------- |
| `id`         | Integer       | primary key                |
| `first_name` | String(155)   | not null                   |
| `last_name`  | String(155)   | not null                   |
| `email`      | String(200)   | unique, not null           |
| `password`   | String(200)   | not null, bcrypt hash      |

`Costumer.check_password(password)` verifies a plaintext password against the
stored hash.

### `products` (`models/product.py` – `Product`)

| Column  | Type        | Constraints  |
| ------- | ----------- | ------------ |
| `id`    | Integer     | primary key  |
| `name`  | String(200) | not null     |
| `price` | Float       | not null     |

Relationship: `Product.orders` → list of `ProductOrder`
(`cascade="all, delete-orphan"`).

### `orders` (`models/order.py` – `Order`)

| Column        | Type    | Constraints                         |
| ------------- | ------- | ----------------------------------- |
| `id`          | Integer | primary key                         |
| `product_id`  | Integer | FK → `products.id`, not null        |
| `costumer_id` | Integer | FK → `costumers.id`, not null       |
| `quantity`    | Integer | not null                            |

Relationship: `Order.products` → list of `ProductOrder`
(`cascade="all, delete-orphan"`).

### `productorders` (`models/product_order.py` – `ProductOrder`)

Join table implementing the many-to-many link between orders and products.

| Column       | Type    | Constraints                                            |
| ------------ | ------- | ------------------------------------------------------ |
| `order_id`   | Integer | FK → `orders.id`, part of composite primary key        |
| `product_id` | Integer | FK → `products.id` (`ondelete="CASCADE"`), part of composite primary key |
| `quantity`   | Integer | not null                                               |

Relationships: `ProductOrder.product` ↔ `Product.orders` and
`ProductOrder.order` ↔ `Order.products` (`back_populates` on both sides).

**Cascade delete:** deleting an `Order` or a `Product` through the ORM removes
its associated `ProductOrder` rows (`delete-orphan`); the `product_id` FK on
`productorders` is additionally declared with `ON DELETE CASCADE` at the
database level.

## Testing

Tests use Python's built-in `unittest` and live in `tests/`. Each test builds
the app with `create_app()`, creates the tables, and drops them afterwards.

```bash
python -m unittest discover tests
```

## Authors

See the `AUTHORS` file:

- Aminat Wakil
- Abdellah syani
