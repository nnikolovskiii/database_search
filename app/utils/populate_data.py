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

conn.commit()
cursor.close()
conn.close()
