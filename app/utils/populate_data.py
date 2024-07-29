import psycopg2
import random
from faker import Faker

fake = Faker()

db_config = {
    'dbname': 'sample-database',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**db_config)
cursor = conn.cursor()


def random_date(start, end):
    return fake.date_between_dates(date_start=start, date_end=end)


def random_rating():
    return random.randint(1, 5)


# Insert data into Users table
i = 0
usernames = set()
emails = set()
users = []
while i < 1000:
    fake_username = fake.user_name()
    fake_email = fake.email()
    if fake_username not in usernames and fake_email not in emails:
        users.append((i, fake_username, fake_email, fake.password(), fake.date_time_this_decade()))
        usernames.add(fake_username)
        emails.add(fake_email)
        i += 1

cursor.executemany(
    "INSERT INTO users (user_id,username, email, password_hash, created_at) VALUES (%s , %s, %s, %s, %s)",
    users
)


# Insert data into Products table
products = []
for _ in range(1000):
    products.append((fake.word(), fake.text(), round(random.uniform(10.0, 1000.0), 2), random.randint(1, 10)))

cursor.executemany(
    "INSERT INTO Products (name, description, price, category_id) VALUES (%s, %s, %s, %s)",
    products
)

# Insert data into Orders table
orders = []
for _ in range(1000):
    orders.append((random.randint(1, 1000), random_date(datetime(2020, 1, 1), datetime(2024, 7, 28)),
                   fake.random_element(elements=('pending', 'completed', 'cancelled')), round(random.uniform(20.0, 2000.0), 2)))

cursor.executemany(
    "INSERT INTO Orders (user_id, order_date, status, total) VALUES (%s, %s, %s, %s)",
    orders
)

# Insert data into OrderItems table
order_items = []
for _ in range(1000):
    order_items.append((random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 10), round(random.uniform(10.0, 1000.0), 2)))

cursor.executemany(
    "INSERT INTO OrderItems (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
    order_items
)

# Insert data into Payments table
payments = []
for _ in range(1000):
    payments.append((random.randint(1, 1000), random_date(datetime(2020, 1, 1), datetime(2024, 7, 28)), round(random.uniform(20.0, 2000.0), 2), fake.random_element(elements=('credit_card', 'paypal', 'bank_transfer'))))

cursor.executemany(
    "INSERT INTO Payments (order_id, payment_date, amount, method, status) VALUES (%s, %s, %s, %s, 'completed')",
    payments
)

# Insert data into Carts table
carts = []
for _ in range(1000):
    carts.append((random.randint(1, 1000), random_date(datetime(2020, 1, 1), datetime(2024, 7, 28))))

cursor.executemany(
    "INSERT INTO Carts (user_id, created_at) VALUES (%s, %s)",
    carts
)

# Insert data into CartItems table
cart_items = []
for _ in range(1000):
    cart_items.append((random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 10)))

cursor.executemany(
    "INSERT INTO CartItems (cart_id, product_id, quantity) VALUES (%s, %s, %s)",
    cart_items
)

# Insert data into Categories table
categories = []
for _ in range(100):
    categories.append((fake.word(),))

cursor.executemany(
    "INSERT INTO Categories (name) VALUES (%s)",
    categories
)

# Insert data into Reviews table
reviews = []
for _ in range(1000):
    reviews.append((random.randint(1, 1000), random.randint(1, 1000), random_rating(), fake.text(), random_date(datetime(2020, 1, 1), datetime(2024, 7, 28))))

cursor.executemany(
    "INSERT INTO Reviews (user_id, product_id, rating, comment, created_at) VALUES (%s, %s, %s, %s, %s)",
    reviews
)

# Insert data into Addresses table
addresses = []
for _ in range(1000):
    addresses.append((random.randint(1, 1000), fake.street_address(), fake.secondary_address(), fake.city(), fake.state(), fake.country(), fake.postcode()))

cursor.executemany(
    "INSERT INTO Addresses (user_id, line1, line2, city, state, country, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    addresses
)

# Insert data into PaymentMethods table
payment_methods = []
for _ in range(1000):
    payment_methods.append((random.randint(1, 1000), fake.credit_card_number(), fake.name(), fake.credit_card_expire(), fake.credit_card_security_code(), random.randint(1, 1000)))

cursor.executemany(
    "INSERT INTO PaymentMethods (user_id, card_number, card_holder_name, expiry_date, cvv, billing_address_id) VALUES (%s, %s, %s, %s, %s, %s)",
    payment_methods
)

# Insert data into Shipments table
shipments = []
for _ in range(1000):
    shipments.append((random.randint(1, 1000), random_date(datetime(2020, 1, 1), datetime(2024, 7, 28)), random_date(datetime(2020, 1, 1), datetime(2024, 7, 28)), fake.random_element(elements=('pending', 'shipped', 'delivered', 'cancelled'))))

cursor.executemany(
    "INSERT INTO Shipments (order_id, shipped_date, delivery_date, status) VALUES (%s, %s, %s, %s)",
    shipments
)

# Insert data into Discounts table
discounts = []
for _ in range(100):
    discounts.append((fake.word(), fake.text(), round(random.uniform(5.0, 50.0), 2), random_date(datetime(2020, 1, 1), datetime(2024, 7, 28)), random_date(datetime(2024, 7, 28), datetime(2025, 7, 28))))

cursor.executemany(
    "INSERT INTO Discounts (code, description, discount_percent, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
    discounts
)

# Insert data into ShippingMethods table
shipping_methods = []
for _ in range(100):
    shipping_methods.append((fake.word(), round(random.uniform(5.0, 50.0), 2), fake.sentence()))

cursor.executemany(
    "INSERT INTO ShippingMethods (method_name, cost, estimated_delivery_time) VALUES (%s, %s, %s)",
    shipping_methods
)

# Insert data into ShippingRates table
shipping_rates = []
for _ in range(100):
    shipping_rates.append((random.randint(1, 100), fake.country(), round(random.uniform(5.0, 50.0), 2)))

cursor.executemany(
    "INSERT INTO ShippingRates (shipping_method_id, destination_country, rate) VALUES (%s, %s, %s)",
    shipping_rates
)

conn.commit()
cursor.close()
conn.close()
