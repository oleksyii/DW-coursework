from fastapi import FastAPI
from typing import List
import asyncpg
import asyncio

app = FastAPI()

async def connect_to_db():
    return await asyncpg.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="alex235689",
        database="oltp_dw",
    )

async def fetch_data(query: str):
    conn = await connect_to_db()
    try:
        return await conn.fetch(query)
    finally:
        await conn.close()

async def get_data():
    query = 'SELECT * FROM "user";'
    return await fetch_data(query)

async def get_data_by_id(item_id: int):
    query = f'SELECT * FROM "user" WHERE id = {item_id};'
    return await fetch_data(query)

@app.get("/data/")
async def get_data_endpoint():
    return await get_data()

@app.get("/data/{item_id}")
async def get_data_by_id_endpoint(item_id: int):
    return await get_data_by_id(item_id)
