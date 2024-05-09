
async def fetch_countries(conn):
    query = '''
    SELECT
        c.country_id,
        c.name as country
    FROM country c
    ORDER BY country
    '''
    countries = await conn.fetch(query)
    return countries
