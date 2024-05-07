import asyncpg

async def insert_countries(countries_data):
    # Establish connection to the database
    conn = await asyncpg.connect(user='postgres', password='alex235689', database='oltp_dw', host='localhost')

    try:
        # Insert each country into the country table
        for country in countries_data:
            await conn.execute("INSERT INTO country (name) VALUES ($1)", country["location_name"])
    finally:
        # Close the connection
        await conn.close()