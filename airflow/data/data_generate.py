import pandas as pd
import random
import os
from faker import Faker
import numpy as np

# Initialize Faker instance to generate fake data
fake = Faker()

# Create directories if they don't exist
os.makedirs("data/raw", exist_ok=True)

# Number of records to generate for each dataset
NUM_CUSTOMERS = 100
NUM_PRODUCTS = 50
NUM_ORDERS = 200

# Generate fake customer data
def generate_customers():
    customers = []
    for _ in range(NUM_CUSTOMERS):
        customers.append({
            'customer_id': random.randint(1, NUM_CUSTOMERS),
            'name': fake.name(),
            'email': fake.email(),
            'country': fake.country(),
            'signup_date': fake.date_this_decade().strftime('%Y-%m-%d')
        })
    return pd.DataFrame(customers)

# Generate fake product data
def generate_products():
    products = []
    for _ in range(NUM_PRODUCTS):
        products.append({
            'product_id': random.randint(1, NUM_PRODUCTS),
            'name': fake.bs(),
            'category': random.choice(['Electronics', 'Clothing', 'Books', 'Toys', 'Home Appliances']),
            'cost_price': round(random.uniform(10, 200), 2),
            'selling_price': round(random.uniform(20, 300), 2)
        })
    return pd.DataFrame(products)

# Generate fake order data
def generate_orders():
    orders = []
    for _ in range(NUM_ORDERS):
        customer_id = random.randint(1, NUM_CUSTOMERS)
        product_id = random.randint(1, NUM_PRODUCTS)
        quantity = random.randint(1, 5)
        order_date = fake.date_this_year().strftime('%Y-%m-%d')
        delivery_date = fake.date_this_year().strftime('%Y-%m-%d')
        
        orders.append({
            'order_id': random.randint(1, NUM_ORDERS),
            'customer_id': customer_id,
            'product_id': product_id,
            'quantity': quantity,
            'order_date': order_date,
            'delivery_date': delivery_date
        })
    return pd.DataFrame(orders)

# Generate and save datasets
def generate_and_save_data():
    # Generate customer, product, and order data
    customers_df = generate_customers()
    products_df = generate_products()
    orders_df = generate_orders()

    # Save them to CSV files
    customers_df.to_csv("data/raw/customers.csv", index=False)
    products_df.to_csv("data/raw/products.csv", index=False)
    orders_df.to_csv("data/raw/orders.csv", index=False)

    print("Data generation complete! Raw data files saved in 'data/raw/'.")

if __name__ == "__main__":
    generate_and_save_data()
