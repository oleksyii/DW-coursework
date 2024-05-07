import math as m

DEFAULT_LIMIT = 10

async def getOffsetAndLimit(conn, page: int, limit: int = DEFAULT_LIMIT):
    query = 'select count(*) from game;'
    count = await conn.fetch(query)
    count = count[0].get('count')
    # print(count[0].get('count'))
    print(f'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n {count}, {page}')
    offset = m.floor(limit * (page - 1))
    if offset >= count:
        offset = count - limit
    return offset, limit
    
    

async def getPage(conn, limit: int, offset: int):
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