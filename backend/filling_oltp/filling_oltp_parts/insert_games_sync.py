from datetime import datetime
import requests
import psycopg2
import ast
from faker import Faker


def is_valid_date(date_str):
    try:
        # Attempt to parse the date string
        datetime.strptime(date_str, '%Y-%m-%d')
        return True  # If parsing succeeds, it's a valid date
    except ValueError:
        return False  # If parsing fails, it's not a valid date


def fetch_game_data(app_id):
    url = f"https://store.steampowered.com/api/appdetails?key=C037D8F73D98B1A13C7A4CE76C4825EC&appids={app_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and str(app_id) in data:
            app_data = data[str(app_id)]
            if app_data.get('success', False):
                return app_data.get('data', {})
    return {}


def read_data(filename='steam_games.txt'):
    data = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i >= 50000:
                break
            try:
                parsed_line = ast.literal_eval(line)
                if 'publisher' in parsed_line and 'developer' in parsed_line:
                    data.append(parsed_line)
            except UnicodeDecodeError:
                print(f"Skipping line {line} due to UnicodeDecodeError")
                continue
            except ValueError:
                print(f"Skipping line {line} due to ValueError")
                continue

    return data

def insert_games(data):
    # Establish connection to the database
    conn = psycopg2.connect(
        dbname="oltp_dw",
        user="postgres",
        password="alex235689",
        host="localhost",
        port="5432"
    )

    # Create a cursor object
    cur = conn.cursor()

    # Initialize Faker object
    fake = Faker()

    # Fetch all publisher_ids and developer_ids
    cur.execute("SELECT publisher_id, name FROM publisher")
    publisher_mapping = {row[1]: row[0] for row in cur.fetchall()}

    cur.execute("SELECT developer_id, name FROM developer")
    developer_mapping = {row[1]: row[0] for row in cur.fetchall()}

    def parse_date(date_str):
        try:
            # Attempt to parse the date string
            date_obj = datetime.strptime(date_str, '%d %b, %Y')
            return date_obj.date()  # Return the parsed date object
        except ValueError:
            return None  # If parsing fails, return None


    # Insert data into the game table
    count = 0
    for item in data:
        publisher_id = publisher_mapping.get(item.get('publisher'))
        developer_id = developer_mapping.get(item.get('developer'))
        if publisher_id and developer_id:
            app_id = item.get('id')
            app_data = fetch_game_data(app_id) if count < 100 else None
            # app_data = None
            if app_data:
                count += 1
                image_url = app_data.get('header_image', '')
                description = app_data.get('detailed_description', fake.text(max_nb_chars=200))
                if app_data.get('release_date')['coming_soon'] == False:
                    publication_date = parse_date(app_data.get('release_date')['date'])
                    print(publication_date)
                else:
                    publication_date = None
                    print(publication_date)
            else:
                publication_date = None
                image_url = ''
                description = fake.text(max_nb_chars=200)
               
            # Preping up the arguments for inserting 
            name = item.get('app_name', '')
            
            publication_date = item.get('release_date', None)
            if publication_date and not is_valid_date(publication_date):
                publication_date = None   
                
            price = item.get('price', 0)
            if isinstance(price, float) == False:
                price = 0
            discounted_price = item.get('discount_price', 0)
            app_id = item.get('id', None)
            
            if app_id is None:
                continue
            
            if image_url and description:
                if app_id and publication_date:
                    cur.execute("INSERT INTO game (image_url, name, publication_date, publisher_id, developer_id, price, discounted_price, description, app_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (image_url, name, publication_date, publisher_id, developer_id, price, discounted_price, description, app_id))
                elif publication_date:
                    print('no app id')
                    cur.execute("INSERT INTO game (image_url, name, publication_date, publisher_id, developer_id, price, discounted_price, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (image_url, name, publication_date, publisher_id, developer_id, price, discounted_price, description))
                elif app_id:
                    cur.execute("INSERT INTO game (image_url, name, publisher_id, developer_id, price, discounted_price, description, app_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (image_url, name, publisher_id, developer_id, price, discounted_price, description, app_id))
            else:
                if app_id and publication_date:
                    cur.execute("INSERT INTO game ( name, publication_date, publisher_id, developer_id, price, discounted_price, app_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, publication_date, publisher_id, developer_id, price, discounted_price, app_id))
                elif publication_date:
                    print('no app id')
                    cur.execute("INSERT INTO game (name, publication_date, publisher_id, developer_id, price, discounted_price) VALUES (%s, %s, %s, %s, %s, %s)", (name, publication_date, publisher_id, developer_id, price, discounted_price))
                elif app_id:
                    cur.execute("INSERT INTO game (name, publisher_id, developer_id, price, discounted_price, app_id) VALUES (%s, %s, %s, %s, %s, %s)", (name, publisher_id, developer_id, price, discounted_price, app_id))
                    
    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()
    print('\n\nINSERT WAS SUCCESSFUL')  