import ast
import random
import psycopg2
import json
from datetime import datetime, timedelta

def read_data(num, filename='steam_games.txt'):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= num:
                break
            try:
                parsed_line = ast.literal_eval(line)
                if 'items' in parsed_line:
                    data.append(parsed_line)
            except UnicodeDecodeError:
                    print(f"Skipping line {line} due to UnicodeDecodeError")
                    continue
            except ValueError:
                    print(f"Skipping line {line} due to ValueError")
                    continue
    # result = set()
    # for row in data:
    #     for g in row['items']:
    #         result.add(g)

    return data

def get_db_connection():
    return psycopg2.connect(
        dbname="oltp_dw", 
        user="postgres", 
        password="alex235689", 
        host="localhost"
    )
    
def generate_launch_times(order_date_str):
    # Convert the order date from string to datetime object
    # order_date_val = datetime.strptime(order_date_str, "%Y-%m-%d").date()
    order_date = datetime.combine(order_date_str, datetime.min.time())

    
    # Define the current time
    now = datetime.now()

    # Generate first_launch_time
    # Calculate the difference in days from the order date to now
    days_since_order = (now - order_date).days

    # Choose a random number of days from 0 to days_since_order to add to the order date
    random_days = random.randint(0, days_since_order)
    first_launch_time = order_date + timedelta(days=random_days)

    # Generate last_launch_time
    # Calculate the difference in days from the first_launch_time to now
    days_since_first_launch = (now - first_launch_time).days

    # Choose a random number of days from 0 to days_since_first_launch to add to the first launch date
    if days_since_first_launch > 0:
        random_days = random.randint(0, days_since_first_launch)
    else:
        random_days = 0
    
    last_launch_time = first_launch_time + timedelta(days=random_days, hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))

    return first_launch_time, last_launch_time


def insert_user_game_time(data):
    # data = json.loads(data)
    for user in data:
        user_id_string = user['user_id']
        items = user['items']
        print(user_id_string)
        print(items)

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Get user_id from user table
                cur.execute("SELECT user_id FROM \"user\" WHERE user_id_string = %s", (user_id_string,))
                try:
                    user_id = cur.fetchone()[0]
                except TypeError:
                    continue    

                for item in items:
                    app_id = int(item['item_id'])
                    total_time_minutes = item['playtime_forever']
                    first_launch_time = 0

                    # Get game_id from game table
                    cur.execute("SELECT game_id FROM game WHERE app_id = %s", (app_id,))
                    try:
                        game_id = cur.fetchone()[0]
                    except TypeError:
                        continue

                    cur.execute("""
                        SELECT order_date FROM \"order\"
                        JOIN order_item ON \"order\".order_id = order_item.order_id
                        WHERE \"order\".user_id = %s AND order_item.game_id = %s
                        ORDER BY order_date DESC LIMIT 1
                    """, (user_id, game_id))
                    order_date = cur.fetchone()[0] if cur.rowcount else first_launch_time
                    first_launch, last_launch = generate_launch_times(order_date)
                    
                    # Insert into user_game_time
                    cur.execute("""
                        INSERT INTO user_game_time (user_id, game_id, total_time_minutes, first_launch_time, last_launch_time)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (user_id, game_id, total_time_minutes, first_launch.date(), last_launch))
                    
    print("\nINSERT WAS SUCCESFULL, I hope")