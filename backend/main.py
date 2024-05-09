from decimal import Decimal
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, status
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
from fastapi.responses import FileResponse
import json

from functions import userFunctions as uf
from functions import orderFunctions as of
from functions import reviewFunctions as rf
from functions import gamesFunctions as gf
from functions import countries as c
from functions import metadataFunctions as m
from functions import fillOLTPFunctions as foltp
from functions import fillOLAPFunctions as folap

# from functions.userFunctions import *

from reviews import reviews as rv

from users_store import usersStoreMain as usm


app = FastAPI(redoc_url=None)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Set this to the specific origins you want to allow, or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Set the HTTP methods you want to allow
    allow_headers=["*"],  # Set this to the specific headers you want to allow, or ["*"] to allow all headers

)


globals = {}

async def connect_to_db():
    global globals
    try:
        print(globals['db_conn'])
    except Exception as e:
        globals['db_conn'] =  await asyncpg.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="alex235689",
            database="oltp_dw",
        )
    return globals['db_conn']

async def connect_to_olap_db():
    global globals
    try:
        print(globals['db_olap_conn'])
    except Exception as e:
        globals['db_olap_conn'] =  await asyncpg.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="alex235689",
            database="oltp_dw",
        )
    return globals['db_olap_conn']


async def close_db_connection():
    globals['db_conn']
    if globals['db_conn']:
        await globals['db_conn'].close()


async def lifespan(app: FastAPI):
    # create the db connection pool
    globals['db_conn'] = await connect_to_db()
    print(f'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\ncontex:{globals["db_conn"]}\n\n\n\n\n\n\n')
    yield
    # Clean up bd conection pool
    await close_db_connection()


@app.get("/")
async def root():
    await connect_to_db()
    print(globals["db_conn"])
    return {"message": "Hello World"}


@app.get("/users")
async def get_users(order_by: str = 'name', order_direction: str = 'ASC', num: int = 100, countries: str | None = None):
    # async with conn.acquire() as conn:
    await connect_to_db()
    if (countries):
        countries_array = [int(x) for x in countries.split(",")]
        users = await uf.fetch_users_by_country(globals['db_conn'], order_by, order_direction, num, countries_array) 
    else:
        users = await uf.fetch_users(globals['db_conn'],order_by, order_direction, num)
        
    # return users
    formatted_users = []
    for user in users:
        formatted_user = {
            "id": user["id"],
            "user_id_string": user["username"],
            "name": user["name"],
            "birthDate": user["birth"].isoformat() if user["birth"] else None,
            "gender": user["gender"],
            "registration_date": user["registration_date"].isoformat() if user["registration_date"] else None,
            "country": user["country"],  # Assuming you have a separate table for countries,
            "user_url": user["user_url"]
        }
        formatted_users.append(formatted_user)
    return formatted_users


@app.get("/countries")
async def get_countries():
    conn = await connect_to_db()
    countries = await c.fetch_countries(conn)
    return countries


@app.get("/metadata")
async def get_meta():
    data = await m.read_metadata()
    return data


@app.get("/download")
async def download_file():
    # Path to the file you want to return
    file_path = "C:\\Users\\Alex\\Desktop\\Labs 3 year\\2 term\\DS\\kyrsach\\code\\backend\\data\\metadata_OLAP.json"
    
    # Return the file as a response
    return FileResponse(file_path, media_type='application/octet-stream', filename='file.json')


@app.get("/orders")
async def get_orders(order_by: str = 'order_date', order_direction: str = 'DESC', num: int = 100,
                     status: str | None = None, date_from: str| None = None, date_to:str | None = None):
    conn = await connect_to_db()
    if (status):
        status = [str(x) for x in status.split(",")]
        # print(status, status_array)
    orders = await of.fetch_orders(conn, order_by, order_direction, num, status, date_from, date_to)
    return orders


@app.get("/reviews")
async def get_reviews(order_by: str = 'posted_date', order_direction: str = 'DESC', num: int = 100, 
                      game_name: str | None = None, date_from: str | None = None, date_to: str | None = None, is_only_interacted: bool | None = None):
    conn = await connect_to_db()
    reviews = await rf.fetch_reviews(conn, order_by, order_direction, num, game_name, date_from, date_to, is_only_interacted)
    return reviews


@app.get("/games")
async def get_all_games(order_by: str = 'name', num: int = 100):
    conn = await connect_to_db()
    return  await gf.fetch_all_games(conn, order_by, limit=num)
    


@app.get("/games/{page}")
async def get_items(page: int, passedLimit: Optional[int] = Query(12, ge=1, le=100), username: str|None = None):
    await connect_to_db()
    offset, limit = await gf.getOffsetAndLimit(globals['db_conn'], page, passedLimit)
    if(username):
        data = await gf.getPage(globals['db_conn'], limit, offset, username)
            # Convert price and discounted_price to floats
        formatted_games = []
        for game in data:
            formatted_game = {
                'id': game['id'],
                'title': game['title'],
                'publication_date': game['publication_date'],
                'developer_name': game['developer_name'],
                'publisher_name': game['publisher_name'],
                'price': float(game['price']),
                'discounted_price': float(game['discounted_price']),
                'description': game['description'],
                'image_url': game['image_url'],
                'app_id': game['app_id'],
                'genres': game['genres'],
                'is_owned': game['is_owned'] 
            }
            formatted_games.append(formatted_game)
    else:
        data = await gf.getPage(globals['db_conn'], limit, offset)
            # Convert price and discounted_price to floats
        formatted_games = []
        for game in data:
            formatted_game = {
                'id': game['id'],
                'title': game['title'],
                'publication_date': game['publication_date'],
                'developer_name': game['developer_name'],
                'publisher_name': game['publisher_name'],
                'price': float(game['price']),
                'discounted_price': float(game['discounted_price']),
                'description': game['description'],
                'image_url': game['image_url'],
                'app_id': game['app_id'],
                'genres': game['genres']
            }
            formatted_games.append(formatted_game)
        

        
    return {
        "message": "get your data, my dude",
        "payload": formatted_games
    }
   

# TODO: please end this freaking game fetching!!!!!!!!!!! 
@app.get('/game/{game_id}')
async def get_game(game_id):
    await connect_to_db()
    
    
@app.get('/reviews/{game_id}')
async def get_items(game_id: int):
    conn = await connect_to_db()
    return await rv.getReviews(conn, game_id)
    
    
@app.get('/user')
async def get_user(username: str):
    return {'message': 'its not okay'}\
    
@app.get('/user-by-country')
async def get_users_by_country(country: str, order_by: str = 'name', order_direction: str = 'ASC', num: int = 100):
    oltp_conn = await connect_to_db()
    users = await uf.fetch_users_by_country(conn=oltp_conn, country_name=country, order_by=order_by, order_direction=order_direction, num=num)
    return  users

@app.post("/export")
async def create_export(meta: m.Meta, num: int = None):
    globals['db_olap_conn'] = await connect_to_olap_db()
    # return meta
    
    # Determine the appropriate export function based on the fact type
    export_function = m.export_sales_fact_from_db if meta.fact == 'Sales' else m.export_review_fact_from_db
    
     # Execute the export function to get the query result
    result = await export_function(globals['db_olap_conn'], meta.metrics, meta.dimensions, num)
    
    # Convert the Decimal objects to serializable types (e.g., strings)
    serializable_result = [
        {key: str(value) if isinstance(value, Decimal) else value for key, value in record.items()}
        for record in result
    ]
    
    # Convert the list of dictionaries to JSON format
    json_data = json.dumps(serializable_result)
    
    # Save the JSON data to a file
    file_path = "exported_data.json"
    with open(file_path, "w") as json_file:
        
        json_file.write(json_data)

    temp_filepath = "C:\\Users\\Alex\\Desktop\\Labs 3 year\\2 term\\DS\\kyrsach\\code\\backend\\exported_data.json"
    # Return the file as a response
    return FileResponse(temp_filepath, media_type='application/octet-stream', filename='file.json')

@app.post("/add-user")
async def create_user(user: uf.User):
    await connect_to_db()
    await uf.add_user(globals['db_conn'], user)
    return {"message": "User created successfully"}


@app.post("/fill-oltp")
async def fill_oltp(percents: float = 2):
    percents = percents/100
    await connect_to_db()
    await foltp.fill_oltp(globals["db_conn"], percents)
    return {"message": "it's okay my dude"}

@app.post("/fill-olap")
async def fill_olap():
    await connect_to_db()
    trace = await folap.fill_oltp_using_pan()
    print(trace)
    return {
        "message": "it's okay my dude",
        "trace": trace
    }
    
@app.post("/clear-oltp")
async def clear_oltp():
    await connect_to_db()
    await foltp.clear_OLTP(globals["db_olap_conn"])
    

@app.post("/sing-in")
async def sing_in(user: usm.User):
    userIndex = await usm.registerActiveUser(user.username)
    return {
        "message": 'Activation complete',
        "token": userIndex
    }

@app.delete("/clear-olap")
async def clear_olap():
    await connect_to_db()
    await folap.clear_OLAP(globals["db_olap_conn"])

# "C:\Users\Alex\Desktop\pentaho\data-integration\.Kitchen.bat"
