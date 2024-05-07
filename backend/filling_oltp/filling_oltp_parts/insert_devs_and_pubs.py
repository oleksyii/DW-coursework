import os
import asyncio
import asyncpg
import ast
from faker import Faker
import random


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

    return (set(d['publisher'] for d in data), set(d['developer'] for d in data))

async def insert_publishers_developers(pub_devs):
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

        # Generate fake descriptions
        descriptions = [fake.text(max_nb_chars=200) for _ in range(len(pub_devs[0]) + len(pub_devs[1]))]

        # Fetch all country_ids from the country table
        country_ids = await conn.fetch("SELECT country_id FROM country")
        country_ids = [row['country_id'] for row in country_ids]

        # Sample random country_ids for publishers and developers using pub_country_mapping
        pub_country_mapping = {pub: country_id for pub, country_id in zip(pub_devs[0], random.sample(country_ids, min(len(country_ids), len(pub_devs[0]))))}
        dev_country_mapping = {dev: country_id for dev, country_id in zip(pub_devs[1], random.sample(country_ids, min(len(country_ids), len(pub_devs[1]))))}

        async with conn.transaction():
            # Insert data into the publisher table
            for name in pub_devs[0]:
                # Sample a random country_id
                random_country_id = random.choice(country_ids)
                await conn.execute("INSERT INTO publisher (name, country_id) VALUES ($1, $2)", name, random_country_id)

            # Insert data into the developer table
            for name in pub_devs[1]:
                # Sample a random country_id
                random_country_id = random.choice(country_ids)
                await conn.execute("INSERT INTO developer (name, country_id) VALUES ($1, $2)", name, random_country_id)

    finally:
        # Close the connection
        await conn.close()
        print('\n\nINSERT WAS SUCCESSFUL, I hope')
        
    