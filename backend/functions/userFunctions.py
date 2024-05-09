from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    name: str
    username: str
    registration_date: str
    birthdate: str
    gender: str
    country: str

async def fetch_users(conn, order_by='name', order_direction = 'ASC', num=None):
    if(conn):
        if num > 0 :
            query = """
            SELECT
                u.user_id as id,
                u.name as name,
                u.user_id_string as username,
                u.birth_date as birth ,
                u.gender as gender,
                u.registration_date as registration_date,
                u.user_url as user_url,
                c.name as country
            FROM "user" u
            JOIN country c on u.country_id = c.country_id
            ORDER BY {} {}
            LIMIT $1
            """.format(order_by, order_direction)
            users = await conn.fetch(query, num)
        else:
            query = '''
            SELECT
                u.user_id as id,
                u.name as name,
                u.user_id_string as username,
                u.birth_date as birth ,
                u.gender as gender,
                u.registration_date as registration_date,
                u.user_url as user_url,
                c.name as country
            FROM "user" u
            JOIN country c on u.country_id = c.country_id
            ORDER BY {} {}
            '''.format(order_by, order_direction)
            users = await conn.fetch(query)
        return users


async def fetch_users_by_country(conn, order_by='name', order_direction = 'ASC', num=None, countries = None):
    users = []
    if(conn):
        if countries is None:
            users = await fetch_users(conn, order_by=order_by, order_direction = order_direction, num=num)
        else:
            countries_ids = ','.join(map(str, countries))
            
            if num != -1 :
                query = """
                SELECT
                    u.user_id as id,
                    u.name as name,
                    u.user_id_string as username,
                    u.birth_date as birth,
                    u.gender as gender,
                    u.registration_date as registration_date,
                    u.user_url as user_url,
                    c.name as country
                FROM "user" u
                JOIN country c on u.country_id = c.country_id
                WHERE c.country_id = ANY($1)
                ORDER BY {} {}
                LIMIT $2
                """.format(order_by, order_direction)
                print(query)
                users = await conn.fetch(query, countries, num)
            else:
                query = '''
                SELECT
                    u.user_id as id,
                    u.name as name,
                    u.user_id_string as username,
                    u.birth_date as birth ,
                    u.gender as gender,
                    u.registration_date as registration_date,
                    u.user_url as user_url,
                    c.name as country
                FROM "user" u
                JOIN country c on u.country_id = c.country_id
                WHERE c.country_id IN ($1)
                ORDER BY {} {}
                '''.format(order_by, order_direction)
                users = await conn.fetch(query, countries)
    return users

async def add_user(conn, user):
      # Extract country_id from the country name
    country_id_query = "SELECT country_id FROM country WHERE name = $1"
    country_row = await conn.fetchrow(country_id_query, user.country)
    if country_row:
        country_id = country_row["country_id"]
    else:
        raise HTTPException(status_code=404, detail="Country not found")
    print(country_id)
    # Insert user data into the user table
    user_insert_query = """
        INSERT INTO "user" (name, birth_date, registration_date, gender, country_id, user_id_string, user_url)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    """
    birthdate = datetime.strptime(user.birthdate, '%Y-%m-%d').date()
    registration_date = datetime.strptime(user.registration_date, '%Y-%m-%d').date()
    user_url = f'http://steamcommunity.com/profiles/{user.username}'
    await conn.execute(
        user_insert_query,
        user.name,
        birthdate,
        registration_date,  # Assuming date in the User model corresponds to birth_date in the table
        user.gender,
        country_id,
        user.username,
        user_url
    )
    

    