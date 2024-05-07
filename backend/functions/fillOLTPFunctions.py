from filling_oltp import insert_main as i

from clearing_dbs import clearDB

async def fill_oltp(conn, percent):
    await clearDB.execute_delete(conn)
    await i.run(percent)
    
async def clear_OLTP(conn):
    await clearDB.execute_delete(conn)