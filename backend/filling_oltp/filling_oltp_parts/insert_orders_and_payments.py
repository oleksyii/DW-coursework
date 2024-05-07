import psycopg2
from faker import Faker
import random
import time

fake = Faker()

def fetch_last_order_id():
    conn = psycopg2.connect(
        dbname="oltp_dw",
        user="postgres",
        password="alex235689",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT MAX(order_id) FROM \"order\"")
        last_order_id = cur.fetchone()[0]
        return last_order_id if last_order_id else 0
    finally:
        cur.close()
        conn.close()

def fetch_user_games():
    conn = psycopg2.connect(
        dbname="oltp_dw",
        user="postgres",
        password="alex235689",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT u.user_id, u.registration_date, ug.game_id 
            FROM "user" u 
            JOIN user_game ug ON u.user_id = ug.user_id
            ORDER BY user_id
        """)
        rows = cur.fetchall()
        user_games = {}
        for row in rows:
            if row[0] in user_games:
                user_games[row[0]]['games'].append(row[2])
            else:
                user_games[row[0]] = {'registration_date': row[1], 'games': [row[2]]}
        return user_games
    finally:
        cur.close()
        conn.close()

def fetch_all_users_and_games():
    conn = psycopg2.connect(
        dbname="oltp_dw",
        user="postgres",
        password="alex235689",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM \"user\"")
        users = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT game_id FROM game")
        games = [row[0] for row in cur.fetchall()]
        return users, games
    finally:
        cur.close()
        conn.close()

def generate_fake_order_data(user_games, all_users, all_games, num_random_orders):
    orders = []
    order_items = []
    payments = []
    last_order_id = fetch_last_order_id() + 1

    # First, handle user_games specific orders
    for user_id, details in user_games.items():
        games = details['games']
        random.shuffle(games)

        while games:
            order_date = fake.date_time_between_dates(datetime_start=details['registration_date'], datetime_end="now")
            order_id = last_order_id
            last_order_id += 1

            orders.append((order_id, user_id, "Completed", order_date, None))

            num_items_in_order = random.randint(1, min(3, len(games)))
            games_for_this_order = [games.pop() for _ in range(num_items_in_order)]

            for idx, game_id in enumerate(games_for_this_order, start=1):
                game_price = fake.random_number(digits=2)
                game_commission = game_price * 0.1
                item_order = idx
                order_items.append((order_id, game_id, game_price, game_commission, item_order))

            payment_date = order_date
            amount = sum(item[2] for item in order_items if item[0] == order_id)
            payments.append((order_id, payment_date, amount))

    # Now, generate random orders with random statuses
    for _ in range(num_random_orders):
        user_id = random.choice(all_users)
        game_id = random.choice(all_games)
        status = random.choice(["Pending", "Cancelled"])
        order_date = fake.date_between(start_date="-2y", end_date="now")
        cancel_date = order_date if status == "Cancelled" else None
        order_id = last_order_id
        last_order_id += 1

        orders.append((order_id, user_id, status, order_date, cancel_date))
        game_price = fake.random_number(digits=2)
        game_commission = game_price * 0.1
        item_order = 1
        order_items.append((order_id, game_id, game_price, game_commission, item_order))
        payment_date = order_date if status == "Pending" else None
        amount = game_price if status == "Pending" else 0
        payments.append((order_id, payment_date, amount))

    return orders, order_items, payments

def insert_data(orders, order_items, payments):
    conn = psycopg2.connect(
        dbname="oltp_dw",
        user="postgres",
        password="alex235689",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    try:
        cur.executemany("INSERT INTO \"order\" (order_id, user_id, status, order_date, cancel_date) VALUES (%s, %s, %s, %s, %s)", orders)
        cur.executemany("INSERT INTO order_item (order_id, game_id, game_price, game_commission, item_order) VALUES (%s, %s, %s, %s, %s)", order_items)
        cur.executemany("INSERT INTO payment (order_id, payment_date, amount) VALUES (%s, %s, %s)", payments)
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred while inserting data: {e}")
    finally:
        cur.close()
        conn.close()