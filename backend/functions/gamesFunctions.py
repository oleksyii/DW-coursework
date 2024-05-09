import math as m
from multipledispatch import dispatch
import asyncpg

DEFAULT_LIMIT = 10

async def getOffsetAndLimit(conn: asyncpg.Connection, page: int, limit: int = DEFAULT_LIMIT):
    query = 'select count(*) from game;'
    count = await conn.fetch(query)
    count = count[0].get('count')
    offset = m.floor(limit * (page - 1))
    if offset >= count:
        offset = count - limit
    return offset, limit
    
    
@dispatch(asyncpg.Connection, int, int)
async def getPage(conn: asyncpg.Connection, limit: int, offset: int):
    query = '''
        select
            g.game_id as id,
            g.name as title,
            g.publication_date,
            d.name as developer_name,
            p.name as publisher_name,
            g.price,
            g.discounted_price,
            g.description,
            g.image_url,
            g.app_id as app_id,
            ARRAY_AGG(g2.name) as genres
        from game g
        join public.developer d on g.developer_id = d.developer_id
        join public.publisher p on p.publisher_id = g.publisher_id
        join public.game_genre gg on g.game_id = gg.game_id
        join public.genre g2 on gg.genre_id = g2.genre_id
        group by g.game_id, g.name, g.publication_date, d.name, p.name, g.price, g.discounted_price, g.description, g.image_url, g.app_id
        order by g.game_id
        limit $1
        offset $2;
    '''
    countries = await conn.fetch(query, limit, offset)
    return countries    


@dispatch(asyncpg.Connection, int, int, str)
async def getPage(conn: asyncpg.Connection, limit: int, offset: int, username: str):
    query = '''
        select
            u.user_id
        from "user" u
        where u.user_id_string = $1;
    '''
    
    row = await conn.fetchrow(query, username)
    # Extract the user_id from the row, if it exists
    if row:
        user_id = row['user_id']
        print(user_id)
    else:
        print("User not found")
        
    query = '''
        select
            g.game_id as id,
            g.name as title,
            g.publication_date,
            d.name as developer_name,
            p.name as publisher_name,
            g.price,
            g.discounted_price,
            g.description,
            g.image_url,
            g.app_id as app_id,
            ARRAY_AGG(g2.name) as genres,
            CASE
                WHEN ug.user_id IS NOT NULL THEN TRUE
                ELSE FALSE
            END AS is_owned
        from game g
        join public.developer d on g.developer_id = d.developer_id
        join public.publisher p on p.publisher_id = g.publisher_id
        join public.game_genre gg on g.game_id = gg.game_id
        join public.genre g2 on gg.genre_id = g2.genre_id
        LEFT JOIN
            user_game ug ON g.game_id = ug.game_id AND ug.user_id = $1
        group by g.game_id, g.name, g.publication_date, d.name, p.name, g.price, g.discounted_price, g.description, g.image_url, g.app_id, ug.user_id
        order by g.game_id
        limit $2
        offset $3;
    '''
    countries = await conn.fetch(query, user_id, limit, offset)
    return countries    


async def fetch_all_games(conn: asyncpg.Connection, order_by: str, limit: int):
    query = """
        select 
            g.name as name
        from game g
        order by $1
        limit $2
    """
    
    return await conn.fetch(query, order_by, limit)