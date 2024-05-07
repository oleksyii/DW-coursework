from datetime import datetime, timedelta
import psycopg2
import ast
from faker import Faker
import random

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def read_data(filename, num):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= num:
                break
            try:
                parsed_line = ast.literal_eval(line)
                if 'user_id' in parsed_line:
                    data.append(parsed_line)
            except UnicodeDecodeError:
                print(f"Skipping line {line} due to UnicodeDecodeError")
                continue
            except ValueError:
                print(f"Skipping line {line} due to ValueError")
                continue

    return data

def insert_users_and_reviews(users_data):
    conn = psycopg2.connect(
        dbname="oltp_dw",
        user="postgres",
        password="alex235689",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()
    fake = Faker()
    user_ids = set()

    for user_data in users_data:
        user_id = user_data['user_id']
        if user_id in user_ids:
            print(f"User {user_id} is already present, probably duplicate, skip")
            continue
        user_ids.add(user_id)
        # if not isinstance(user_id, int):
        #     print('skip')
        #     continue
        name = fake.name()
        birth_date = fake.date_of_birth(minimum_age=11, maximum_age=70)
        
        # Find the first review posted by the user
        first_review_posted_date = datetime.now()
        for review_data in user_data['reviews']:
            try:
                posted_date = datetime.strptime(review_data['posted'], 'Posted %B %d, %Y.')
            except ValueError:
                print(f"Date {posted_date} is wicked. Skipping review insertion")
                continue
            if posted_date < first_review_posted_date:
                first_review_posted_date = posted_date
        
        # Generate registration_date such that it's smaller than the time of the first review posted
        registration_date = fake.date_time_between(start_date='-5y', end_date=first_review_posted_date)

        gender = random.choice(['male', 'female'])
        
        # Execute the query to get the minimum country_id
        cur.execute("SELECT MIN(country_id) AS min_index FROM country;")
        min_index = cur.fetchone()[0]
        print("Minimum index:", min_index)

        # Execute the query to get the maximum country_id
        cur.execute("SELECT MAX(country_id) AS max_index FROM country;")
        max_index = cur.fetchone()[0]
        print("Maximum index:", max_index)
        
        country_id = random.randint(min_index, max_index)

        user_url = user_data['user_url']
        cur.execute("INSERT INTO \"user\" (user_id_string, name, birth_date, gender, registration_date, country_id, user_url) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (user_id, name, birth_date, gender, registration_date, country_id, user_url))

        for review_data in user_data['reviews']:
            game_id = review_data['item_id']
                        
            # Check if game_id exists as app_id in the game table
            cur.execute("SELECT game_id FROM game WHERE app_id = %s", (game_id,))
            row = cur.fetchone()
            if row is None:
                print(f"Game with ID {game_id} not found in game table. Skipping review insertion.")
                continue
            # get the actual game_id in DB
            game_id_actual = row[0]
            try:
                posted_date = datetime.strptime(review_data['posted'], 'Posted %B %d, %Y.')
            except ValueError:
                print(f"Date {posted_date} is wicked. Skipping review insertion")
                continue
            last_interaction_update = posted_date + timedelta(days=random.randint(1, 365))            
            # Convert recommend to 1 if True, else 0
            recommend = 1 if review_data['recommend'] else 0
            
            # Parse funny and helpful attributes
            funny_str = review_data['funny']
            helpful_str = review_data['helpful']
            
            # Extract number of funny interactions
            funny_count = 0
            if funny_str:
                try:
                    funny_count = int(funny_str.split()[0])
                except ValueError:
                    # print(f"Invalid funny count: {funny_str}. Setting to 0.")
                    funny_count = 0
            
            # Extract number of helpful interactions
            helpful_count = 0
            if helpful_str:
                try:
                    helpful_count = int(helpful_str.split()[0])
                except ValueError:
                    # print(f"Invalid helpful count: {helpful_str}. Setting to 0.")
                    helpful_count = 0
            
            total_interactions_count = 0
            if helpful_str:
                try:
                    total_interactions_count = int(helpful_str.split()[2])
                except ValueError:
                    print(f"Invalid helpful count: {helpful_str}. Setting to 0.")
            # Calculate total interactions count
            interactions_count = funny_count + helpful_count + (total_interactions_count - helpful_count)
            
            cur.execute("INSERT INTO review (user_id, game_id, posted_date, recommend, review_text, funny_count, useful_count, interactions_count, last_interaction_update, game_id_actual) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (user_id, game_id, posted_date, recommend, review_data['review'], funny_count, helpful_count, interactions_count, last_interaction_update, game_id_actual))

    conn.commit()
    cur.close()
    conn.close()
    print('\n\nINSERT WAS SUCCESSFUL')