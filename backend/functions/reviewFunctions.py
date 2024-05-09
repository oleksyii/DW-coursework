
import asyncpg


async def fetch_reviews(conn: asyncpg.Connection, order_by, order_direction, num,
                         game_name: str | None = None, date_from: str | None = None, date_to: str | None = None,
                         is_only_interacted: bool | None = None):
    if(conn):
        where_part = """
            where
        """ if (game_name or date_from or date_to or is_only_interacted) else ""
        
        print(where_part)
        
        if game_name:
            where_part += f"g.name LIKE '%{game_name}%' and "
        if date_from and not date_to:
            where_part += f"r.posted_date > '{date_from}' and "
        if date_from and date_to:
            where_part += f"r.posted_date BETWEEN '{date_from}' and '{date_to}' and "    
        if is_only_interacted:
            where_part += "r.interactions_count > 0 and "    
        where_part = where_part[:-4]
        select_from_part = """
            select
                u.name as name,
                u.user_id_string as username,
                g.name as game,
                r.posted_date as posted_date,
                r.funny_count as funny_count,
                r.useful_count as useful_count,
                r.interactions_count,
                CASE
                    WHEN r.recommend = 1 THEN TRUE
                    ELSE FALSE
                END AS recommend
            from review r
            join public.game g on r.game_id = g.app_id
            join public."user" u on u.user_id_string = r.user_id
        """
        
        select_from_part += where_part
        
        print(select_from_part)
        
        if num > 0:
            if (game_name):
                query = """
                {}
                order by 
                    similarity(g.name, '{}') DESC,
                    {} {}
                LIMIT $1;
                """.format(select_from_part, game_name, order_by, order_direction)
            else:
                query = """
                {}
                order by {} {}
                LIMIT $1;
                """.format(select_from_part, order_by, order_direction)
            result = await conn.fetch(query, num)
        else:
            query = '''
            select
                u.name as name,
                u.user_id_string as username,
                g.name as game,
                r.posted_date as posted_date,
                r.funny_count as funny_count,
                r.useful_count as useful_count,
                r.interactions_count,
                CASE
                    WHEN r.recommend = 1 THEN TRUE
                    ELSE FALSE
                END AS recommend
            from review r
            join public.game g on r.game_id = g.app_id
            join public."user" u on u.user_id_string = r.user_id
            order by {} {};
            '''.format(order_by, order_direction)
            result = await conn.fetch(query)
        return result