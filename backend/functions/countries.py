
async def fetch_countries(conn):
    query = '''
    SELECT
        c.name as country
    FROM country c
    '''
    countries = await conn.fetch(query)
    return countries    