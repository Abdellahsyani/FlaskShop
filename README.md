# Flaskshop -  project on API for payment on FlaskShop Web App

# Introduction


# Purpose of the Project

The project focuses on creating an e-commerce API using Flask. Its purpose is to provide users with a safe and convenient way to shop from home. By using this API, users can securely browse and purchase their favorite products without worrying about their personal information being stolen by attackers. The platform eliminates the need for long trips to physical stores, allowing users to easily shop from their phones and complete transactions effortlessly from the comfort of their home

## Database Schema

Customers: Stores user information such as personal details, login credentials, and payment information.
Products: Contains product details including names, descriptions, prices, and availability.
Orders: Tracks customer orders, including product selections, quantities, and order statuses.

## Setting Up the Flask Server

To get started with the e-commerce API, follow these steps to set up the Flask server:

1. Install Flask
Make sure you have Flask installed. You can do this by running:

pip install Flask

2. Create the Flask Application
In the main project directory, create a file called app.py and initialize the Flask application. Here's an example setup:

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the e-commerce API!"

if __name__ == '__main__':
    app.run(debug=True)

3. Run the Server
After setting up the application, you can start the Flask server by running:

python app.py

The server will now be running locally, and you can access the API by navigating to http://127.0.0.1:5000/ in your browser.


## endpoint/routes
