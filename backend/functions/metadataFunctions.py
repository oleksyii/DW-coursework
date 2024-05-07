
import json
from pydantic import BaseModel

METADATA_PATH = 'C:\\Users\\Alex\\Desktop\\Labs 3 year\\2 term\\DS\\kyrsach\\code\\backend\\data\\metadata_OLAP.json'

class Meta(BaseModel):
    fact: str
    dimensions: list
    metrics: list

async def read_metadata():
    def read_file(file_name):
        file_handle = open(file_name)
        data = file_handle.read()
        file_handle.close()
        formatted_data = json.loads(data)
        return formatted_data
    # global METADATA_PATH
    # print(file_name)
    
    return read_file(METADATA_PATH)

# 
async def export_sales_fact_from_db(conn, metrics: list, dimensions: list, num: int = None):
    tables_dict = {       
        "game": ["gd.name as game_name", "game_name"],
        "genre": ["ged.name as genre_name", "genre_name"],
        "date": ["dad.event_date as event_date", "event_date"],
        "developer": ["dd.name as dev_name", "dev_name"],
        "developer->country": ["dd.country_name as dev_country", "dev_country"],
        "publisher": ["pd.name as pub_name", "pub_name"],
        "publisher->country": ["pd.country_name as pub_country", "pub_country"],
        "user": ["ud.username as username", "username"],
        "user->gender": ["ud.gender as gender", "gender"],
        "country": ["ld.location_name as country", "country"],
        
    }
    
    def construct_sql_query(select_values, num=None):
        # Construct the SELECT part of the query
        select_metrics_part = "SELECT\n"
        select_metrics_part += ",\n".join([f"    {'SUM' if value in ['game_price', 'game_commission', 'recommend'] else 'AVG'}(sf.{value}) as {value}" for value in select_values])
        
        # join by dict of tables
        select_dims_part = ',\n' if len(select_values) > 0 else '\n'
        select_dims_part += ",\n".join(tables_dict[dim][0] for dim in dimensions)
        
        from_joins_part = '''
        from sales_fact sf
            join developer_dim dd on sf.developer_id = dd.developer_id
            join publisher_dim pd on sf.publisher_id = pd.publisher_id
            join game_dim gd on sf.game_id = gd.game_id
            join game_genre_bridge ggb on gd.game_id = ggb.game_id
            join genre_dim ged on ggb.genre_id = ged.genre_id
            join date_dim dad on sf.date_id = dad.date_id
            join user_dim ud on sf.user_id = ud.user_id
            join public.location_dim ld on sf.country_id = ld.location_id
        '''
        
        # Construct the GROUP BY part of the query
        group_by_query = "\nGROUP BY " + ", ".join(tables_dict[dim][1] for dim in dimensions)
        
        
        # Construct the LIMIT part of the query
        limit_query = f"\nLIMIT {num};" if num  else ';'
        
        # Combine all parts of the query
        sql_query = select_metrics_part + select_dims_part + from_joins_part + group_by_query + limit_query
        print(f'\n\n\n\n\n\n\n\n\n\n{sql_query}')
        
        return sql_query
    
    if(conn):
        query = construct_sql_query(metrics, num)
        res = await conn.fetch(query)
        return res


async def export_review_fact_from_db(conn, metrics: list, dimensions: list, num: int = None):
    tables_dict = {       
        "game": ["gd.name as game_name", "game_name"],
        "game->genre": ["ged.name as genre_name", "genre_name"],
        "game->publisher": ["pd.name as pub_name", "pub_name"],
        "game->developer": ["dd.name as dev_name", "dev_name"],
        "game->publisher->country": ["pd.country_name as pub_country", "pub_country"],
        "game->developer->country": ["dd.country_name as dev_country", "dev_country"],
        "user": ["ud.username as username", "username"],
        "user->gender": ["ud.gender as gender", "gender"],
        "user->country": ["ud.country_name as country", "country"],
        "date": ["dad.event_date as event_date", "event_date"],
        
    }
    
    def construct_sql_query(select_values, num=None):
        # Construct the SELECT part of the query
        select_metrics_part = "SELECT\n"
        select_metrics_part += ",\n".join([f"    AVG(rf.{value}) as {value}" for value in select_values])
        
        # join by dict of tables
        select_dims_part = ',\n' if len(select_values) > 0 else '\n'
        select_dims_part += ",\n".join(tables_dict[dim][0] for dim in dimensions)
        
        from_joins_part = '''
        from review_fact rf
            join game_dim gd on rf.game_id = gd.game_id
            join developer_dim dd on gd.developer_id = dd.developer_id
            join publisher_dim pd on gd.publisher_id = pd.publisher_id
            join game_genre_bridge ggb on gd.game_id = ggb.game_id
            join genre_dim ged on ggb.genre_id = ged.genre_id
            join date_dim dad on rf.date_id = dad.date_id
            join user_dim ud on rf.user_id = ud.user_id
        '''
        
        # Construct the GROUP BY part of the query
        group_by_query = "\nGROUP BY " + ", ".join(tables_dict[dim][1] for dim in dimensions)
        
        
        # Construct the LIMIT part of the query
        limit_query = f"\nLIMIT {num};" if num  else ';'
        
        # Combine all parts of the query
        sql_query = select_metrics_part + select_dims_part + from_joins_part + group_by_query + limit_query
        print(f'\n\n\n\n\n\n\n\n\n\n{sql_query}')
        
        return sql_query
    
    if(conn):
        query = construct_sql_query(metrics, num)
        res = await conn.fetch(query)
        return res
