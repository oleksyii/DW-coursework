import asyncio
import os
import asyncpg
import json
from concurrent.futures import ThreadPoolExecutor

from filling_oltp.filling_oltp_parts import insert_countries as ic
from filling_oltp.filling_oltp_parts import insert_devs_and_pubs as idp
from filling_oltp.filling_oltp_parts import insert_games as ig
from filling_oltp.filling_oltp_parts import insert_games_sync as igo
from filling_oltp.filling_oltp_parts import insert_users_and_reviews as iuar
from filling_oltp.filling_oltp_parts import insert_genres as igr
from filling_oltp.filling_oltp_parts import insert_game_genres as iggr
from filling_oltp.filling_oltp_parts import insert_user_games as iug
from filling_oltp.filling_oltp_parts import insert_orders_and_payments as ioap
from filling_oltp.filling_oltp_parts import insert_user_playtime as iupt

executor = ThreadPoolExecutor()

PATH_TO_COUNTRIES = "C:\\Users\\Alex\\Desktop\\Labs 3 year\\2 term\\DS\\kyrsach\\code\\backend\\data\\countries.json"
PATH_TO_GAMES = "C:\\Users\\Alex\\Desktop\\Labs 3 year\\2 term\\DS\\kyrsach\\code\\backend\\data\\steam_games.txt"
PATH_TO_REVIEWS = "C:\\Users\\Alex\\Desktop\\Labs 3 year\\2 term\\DS\\kyrsach\\code\\backend\\data\\australian_user_reviews.txt"
PATH_TO_USER_ITEMS = "C:\\Users\\Alex\\Desktop\\Labs 3 year\\2 term\\DS\\kyrsach\\code\\backend\\data\\australian_users_items.txt"
        
async def main(percent):
    num = 1000 * percent
    
    # COUNTRIES
    with open(PATH_TO_COUNTRIES, "r") as file:
        countries_data = json.load(file)
    
    # Execute the insert_countries function
    await ic.insert_countries(countries_data)
    
    # PUB DEVS
    publishers_and_developers = await idp.read_data(PATH_TO_GAMES)
    print("Publishers:", publishers_and_developers[0])
    print("Developers:", publishers_and_developers[1])
    await idp.insert_publishers_developers(publishers_and_developers)
    
    
    # GAMES
    def insert_gm():
        data = igo.read_data(PATH_TO_GAMES)
        igo.insert_games(data)
    
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(executor, insert_gm)
    
    
    # USERS AND REVIEWS
    def insert_u_and_r():
        users_data = iuar.read_data(PATH_TO_REVIEWS, num)
        iuar.insert_users_and_reviews(users_data)
    
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(executor, insert_u_and_r)    
    
    
    # GENRES
    def insert_g():
        genres = igr.read_data(PATH_TO_GAMES)
        igr.insert_genres(genres)
    
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(executor, insert_g)   
    
     
    # GENRES AND GAME_GENRES
    def insert_ggr():
        result = iggr.read_data(PATH_TO_GAMES)
        iggr.insert_game_genres(result)
    
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(executor, insert_ggr)   


    # USER GAMES
    def insert_ugm():
        result = iug.read_data(PATH_TO_USER_ITEMS)
        iug.insert_user_games(result)
    
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(executor, insert_ugm)   
      
    
    # ORDERS AND PAYMENTS
    def isnsert_oap():
        user_games = ioap.fetch_user_games()
        all_users, all_games = ioap.fetch_all_users_and_games()
        orders, order_items, payments = ioap.generate_fake_order_data(user_games, all_users, all_games, 50)
        ioap.insert_data(orders, order_items, payments)
    
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(executor, isnsert_oap)   
   
   
    # USER PLAYIME
    def insert_upt():
        file_data = iupt.read_data(num, PATH_TO_USER_ITEMS)
        iupt.insert_user_game_time(file_data)
    
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(executor, insert_upt)  
    
    
    
     
# Run the main function
async def run(percent): 
    await main(percent)