
async def getReviews(conn, game_id):
    query = '''
    select
        u.name,
        r.posted_date,
        r.review_text,
        r.funny_count,
        r.useful_count
    from review r
    join public."user" u on r.user_id = u.user_id_string
    where game_id_actual = $1;
    '''
    countries = await conn.fetch(query, game_id)
    return countries 