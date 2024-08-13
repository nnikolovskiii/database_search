from datetime import datetime

import psycopg2
import random
from faker import Faker

fake = Faker()

db_config = {
    'dbname': 'database_search',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '9871'
}

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()



# def random_date(start, end):
#     return fake.date_between_dates(date_start=start, date_end=end)
#
#
# def random_rating():
#     return random.randint(1, 5)
#
#
# i = 0
# usernames = set()
# emails = set()
# users = []
# while i < 1000:
#     fake_username = fake.user_name()
#     fake_email = fake.email()
#     if fake_username not in usernames and fake_email not in emails:
#         users.append((i, fake_username, fake_email, fake.password(), fake.date_time_this_decade()))
#         usernames.add(fake_username)
#         emails.add(fake_email)
#         i += 1
#
# cursor.executemany(
#     "INSERT INTO users (user_id,username, email, password_hash, created_at) VALUES (%s , %s, %s, %s, %s)",
#     users
# )
#
# categories = [
#     'Technology', 'Health', 'Finance', 'Education', 'Entertainment',
#     'Sports', 'Travel', 'Food', 'Fashion', 'Science',
#     'Automotive', 'Real Estate', 'Books', 'Movies', 'Music',
#     'Art', 'History', 'Nature', 'Photography', 'Gardening',
#     'DIY', 'Pets', 'Parenting', 'Fitness', 'Beauty',
#     'Environment', 'Politics', 'Business', 'Marketing', 'Personal Development',
#     'Relationships', 'Religion', 'Philosophy', 'Law', 'Cooking',
#     'Home Improvement', 'Crafting', 'Adventure', 'Culture', 'Video Games',
#     'Comedy', 'Space', 'Architecture', 'Writing', 'Poetry',
#     'Mythology', 'Social Media', 'Technology Trends', 'Startups', 'Investments'
# ]
#
# category_data = [(i, category) for i, category in enumerate(categories)]
#
#
# cursor.executemany(
#     "INSERT INTO categories (category_id, name) VALUES (%s, %s)",
#     category_data
# )
#
# products = []
# for i in range(1000):
#     products.append((i, fake.word(), fake.text(), round(random.uniform(0.0, 1000.0), 0), random.randint(0, len(categories)-1)))
#
# cursor.executemany(
#     "INSERT INTO Products (product_id, name, description, price, category_id) VALUES (%s, %s, %s, %s, %s)",
#     products
# )
#
# orders = []
# for i in range(1000):
#     orders.append((i, random.uniform(0, 999), random_date(datetime(2020, 1, 1), datetime(2024, 7, 28)),
#                    fake.random_element(elements=('pending', 'completed', 'cancelled')),
#                    round(random.uniform(20.0, 2000.0), 2)))
#
# cursor.executemany(
#     "INSERT INTO Orders (order_id, user_id, order_date, status, total) VALUES (%s, %s, %s, %s, %s)",
#     orders
# )
#
# order_items = []
# for i in range(1000):
#     order_items.append((i, random.uniform(0, 999), random.uniform(0, 999), random.randint(1, 10),
#                         round(random.uniform(10.0, 100000.0), 2)))
#
# cursor.executemany(
#     "INSERT INTO OrderItems (order_item_id, order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s, %s)",
#     order_items
# )
#
# payments = []
# for i in range(1000):
#     payments.append((i, random.uniform(0, 999), random_date(datetime(2020, 1, 1), datetime(2024, 7, 28)),
#                      round(random.uniform(20.0, 2000.0), 2),
#                      fake.random_element(elements=('credit_card', 'paypal', 'bank_transfer'))))
#
# cursor.executemany(
#     "INSERT INTO Payments (payment_id, order_id, payment_date, amount, method, status) VALUES (%s, %s, %s, %s, %s, 'completed')",
#     payments
# )
#
# carts = []
# for i in range(1000):
#     carts.append((i, random.uniform(0, 999), random_date(datetime(2020, 1, 1), datetime(2024, 7, 28))))
#
# cursor.executemany(
#     "INSERT INTO Carts (cart_id, user_id, created_at) VALUES (%s, %s, %s)",
#     carts
# )
#
# cart_items = []
# for i in range(1000):
#     cart_items.append((i, random.uniform(0, 999), random.randint(0, 999), random.randint(1, 10)))
#
# cursor.executemany(
#     "INSERT INTO CartItems (cart_item_id, cart_id, product_id, quantity) VALUES (%s, %s, %s, %s)",
#     cart_items
# )
#
# reviews = []
# for i in range(1000):
#     reviews.append((i, random.uniform(0, 999), random.uniform(0, 999), random_rating(), fake.text(),
#                     random_date(datetime(2020, 1, 1), datetime(2024, 7, 28))))
#
# cursor.executemany(
#     "INSERT INTO Reviews (review_id, user_id, product_id, rating, comment, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
#     reviews
# )
#
# addresses = []
# for i in range(1000):
#     addresses.append((i, random.uniform(0, 999), fake.street_address(), fake.secondary_address(), fake.city(),
#                       fake.state(), fake.country(), fake.postcode()))
#
# cursor.executemany(
#     "INSERT INTO Addresses (address_id, user_id, line1, line2, city, state, country, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#     addresses
# )
#
# payment_methods = []
# for i in range(1000):
#     payment_methods.append((i, random.uniform(0, 999), fake.credit_card_number(), fake.name(), random_date(datetime(2025, 1, 1), datetime(2030, 7, 28)),
#                             fake.credit_card_security_code(), random.uniform(0, 999)))
#
# cursor.executemany(
#     "INSERT INTO PaymentMethods (payment_method_id, user_id, card_number, card_holder_name, expiry_date, cvv, billing_address_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#     payment_methods
# )
#
# shipments = []
# for i in range(1000):
#     shipments.append((i, random.uniform(0, 999), random_date(datetime(2020, 1, 1), datetime(2024, 7, 28)),
#                       random_date(datetime(2020, 1, 1), datetime(2024, 7, 28)),
#                       fake.random_element(elements=('pending', 'shipped', 'delivered', 'cancelled'))))
#
# cursor.executemany(
#     "INSERT INTO Shipments (shipment_id, order_id, shipped_date, delivery_date, status) VALUES (%s, %s, %s, %s, %s)",
#     shipments
# )
#
# discounts = []
# for i in range(300):
#     discounts.append((i, fake.sentence(), round(random.uniform(5.0, 50.0), 2),
#                       random_date(datetime(2020, 1, 1), datetime(2024, 7, 28)),
#                       random_date(datetime(2024, 7, 28), datetime(2025, 7, 28))))
#
# cursor.executemany(
#     "INSERT INTO Discounts (discount_id, description, discount_percent, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
#     discounts
# )
#
# shipping_methods = []
# for i in range(100):
#     shipping_methods.append((i, fake.word(), round(random.uniform(5.0, 50.0), 2), fake.sentence()))
#
# cursor.executemany(
#     "INSERT INTO ShippingMethods (shipping_method_id, method_name, cost, estimated_delivery_time) VALUES (%s, %s, %s, %s)",
#     shipping_methods
# )
#
# shipping_rates = []
# for i in range(1000):
#     shipping_rates.append((i, random.randint(0, 99), fake.country(), round(random.uniform(5.0, 50.0), 2)))
#
# cursor.executemany(
#     "INSERT INTO ShippingRates (shipping_rate_id, shipping_method_id, destination_country, rate) VALUES (%s, %s, %s, %s)",
#     shipping_rates
# )
#

conn.commit()
cursor.close()
conn.close()
