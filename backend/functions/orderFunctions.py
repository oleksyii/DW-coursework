
from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime

class Order(BaseModel):
    username: str
    status: str
    order_date: str
    cancel_date: str
    items: list
    cheque: float

async def fetch_orders(conn, order_by='name', order_direction = 'ASC', num=None):
    if(conn):
        if num:
            query = """
            SELECT
                o.order_id as id,
                u.user_id_string as username,
                o.status as status,
                o.order_date as order_date,
                o.cancel_date as cancel_date,
                STRING_AGG(g.name, ', ') AS games,
                AVG(p.amount) as cheque

            from "order" o
                join public."user" u on u.user_id = o.user_id
                join order_item oi on o.order_id = oi.order_id
                join public.payment p on o.order_id = p.order_id
                join public.game g on g.game_id = oi.game_id

            group by u.name, o.order_id, o.status, o.order_date, o.cancel_date
            order by {} {}
            LIMIT $1;
            """.format(order_by, order_direction)
            result = await conn.fetch(query, num)
        else:
            query = '''
            SELECT
                o.order_id as id,
                u.user_id_string as username,
                o.status as status,
                o.order_date as order_date,
                o.cancel_date as cancel_date,
                STRING_AGG(g.name, ', ') AS games,
                AVG(p.amount) as cheque

            from "order" o
                join public."user" u on u.user_id = o.user_id
                join order_item oi on o.order_id = oi.order_id
                join public.payment p on o.order_id = p.order_id
                join public.game g on g.game_id = oi.game_id

            group by u.name, o.order_id, o.status, o.order_date, o.cancel_date
            order by {} {};
            '''.format(order_by, order_direction)
            result = await conn.fetch(query)
        return result
    
    
async def add_user(conn, user):
    # Insert order data into the order table
    user_insert_query = """
        INSERT INTO "user" (name, birth_date, registration_date, gender, country_id, user_id_string)
        VALUES ($1, $2, $3, $4, $5, $6)
    """
    date_string = user.birthdate
    birthdate = datetime.strptime(user.birthdate, '%Y-%m-%d').date()
    registrationdate = datetime.strptime(user.registrationdate, '%Y-%m-%d').date()
    await conn.execute(
        user_insert_query,
        user.name,
        birthdate,
        registrationdate,  # Assuming date in the User model corresponds to birth_date in the table
        user.gender,
        country_id,
        user.username
    )