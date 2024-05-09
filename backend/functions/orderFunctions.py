
from pydantic import BaseModel
from datetime import datetime
import asyncpg

class Order(BaseModel):
    username: str
    status: str
    order_date: str
    cancel_date: str
    items: list
    cheque: float

async def fetch_orders(conn: asyncpg.Connection, order_by, order_direction, num, 
                       statuses: str | None = None, date_from: str| None = None, date_to:str | None = None):
    if(conn):
        where_part = """
            where
        """ if (statuses or date_from or date_to) else ""
        
        print(where_part)
        
        if statuses:
            where_part += "status = ANY(ARRAY[" + ", ".join([f"'{status}'" for status in statuses]) + "]) and "
        if date_from and not date_to:
            where_part += f"order_date > '{date_from}' and "
        if date_from and date_to:
            where_part += f"order_date BETWEEN '{date_from}' and '{date_to}' and "    
        where_part = where_part[:-4]
        select_from_part = """
            SELECT
                o.order_id as id,
                u.name as name,
                u.user_id_string as username,
                o.status as status,
                o.order_date as order_date,
                o.cancel_date as cancel_date,
                STRING_AGG(g.name, ', ') AS games,
                AVG(p.amount) as sum

            from "order" o
                join public."user" u on u.user_id = o.user_id
                join order_item oi on o.order_id = oi.order_id
                join public.payment p on o.order_id = p.order_id
                join public.game g on g.game_id = oi.game_id
        """
        
        select_from_part += where_part
        if num > 0:
            
            query = """
            {}
            group by id, u.name, username, status, order_date, cancel_date
            order by {} {}
            LIMIT $1;
            """.format(select_from_part, order_by, order_direction)
            print(query)
            result = await conn.fetch(query, num)
        else:
            query = """
            {}
            group by id, u.name, username, status, order_date, cancel_date
            order by {} {}
            """.format(select_from_part, order_by, order_direction)
            print(query)
            result = await conn.fetch(query)
        return result
    

# TODO: Add the order 
async def add_order(conn: asyncpg.Connection, user):
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