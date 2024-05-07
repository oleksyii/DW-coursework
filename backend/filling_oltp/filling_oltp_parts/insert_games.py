from datetime import datetime
import asyncpg
import ast
from faker import Faker


async def is_valid_date(date_str):
    try:
        # Attempt to parse the date string
        datetime.strptime(date_str, '%Y-%m-%d')
        return True  # If parsing succeeds, it's a valid date
    except ValueError:
        return False  # If parsing fails, it's not a valid date

async def fetch_game_data(session, app_id):
    url = f"https://store.steampowered.com/api/appdetails?key=C037D8F73D98B1A13C7A4CE76C4825EC&appids={app_id}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if data and str(app_id) in data:
                app_data = data[str(app_id)]
                if app_data.get('success', False):
                    return app_data.get('data', {})
    return {}

async def read_data(filename='steam_games.txt'):
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

async def insert_games(data):
    # Establish connection to the database
    conn = await asyncpg.connect(
        user="postgres",
        password="alex235689",
        database="oltp_dw",
        host="localhost"
    )
    try:
        # Initialize Faker object
        fake = Faker()

        async with conn.transaction():
            # Fetch all publisher_ids and developer_ids
            publisher_mapping = await conn.fetch("SELECT publisher_id, name FROM publisher")
            publisher_mapping = {row['name']: row['publisher_id'] for row in publisher_mapping}

            developer_mapping = await conn.fetch("SELECT developer_id, name FROM developer")
            developer_mapping = {row['name']: row['developer_id'] for row in developer_mapping}

            for item in data:
                publisher_id = publisher_mapping.get(item.get('publisher'))
                developer_id = developer_mapping.get(item.get('developer'))
                if publisher_id and developer_id:
                    app_id = item.get('id')
                    # app_data = await fetch_game_data(session, app_id)
                    app_data = None
                    if app_data:
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

                    # Preparing the arguments for insertion
                    name = item.get('app_name', '')
                    price = item.get('price', 0)
                    if not isinstance(price, float):
                        price = 0
                    discounted_price = item.get('discount_price', 0)
                    app_id = item.get('id', None)

                    if app_id is None:
                        continue

                    if image_url and description:
                        if app_id and publication_date:
                            await conn.execute("INSERT INTO game (image_url, name, publication_date, publisher_id, developer_id, price, discounted_price, description, app_id) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)", image_url, name, publication_date, publisher_id, developer_id, price, discounted_price, description, app_id)
                        elif publication_date:
                            print('no app id')
                            await conn.execute("INSERT INTO game (image_url, name, publication_date, publisher_id, developer_id, price, discounted_price, description) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)", image_url, name, publication_date, publisher_id, developer_id, price, discounted_price, description)
                        elif app_id:
                            await conn.execute("INSERT INTO game (image_url, name, publisher_id, developer_id, price, discounted_price, description, app_id) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)", image_url, name, publisher_id, developer_id, price, discounted_price, description, app_id)
                    else:
                        if app_id and publication_date:
                            await conn.execute("INSERT INTO game (name, publication_date, publisher_id, developer_id, price, discounted_price, app_id) VALUES ($1, $2, $3, $4, $5, $6, $7)", name, publication_date, publisher_id, developer_id, price, discounted_price, app_id)
                        elif publication_date:
                            print('no app id')
                            await conn.execute("INSERT INTO game (name, publication_date, publisher_id, developer_id, price, discounted_price) VALUES ($1, $2, $3, $4, $5, $6)", name, publication_date, publisher_id, developer_id, price, discounted_price)
                        elif app_id:
                            await conn.execute("INSERT INTO game (name, publisher_id, developer_id, price, discounted_price, app_id) VALUES ($1, $2, $3, $4, $5, $6)", name, publisher_id, developer_id, price, discounted_price, app_id)

    finally:
        # Close the connection
        await conn.close()
        print('\n\nINSERT WAS SUCCESSFUL')