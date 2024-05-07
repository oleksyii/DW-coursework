import asyncpg


async def execute_delete(conn):
    try:
        # Execute the stored procedure
        result = await conn.execute("CALL delete_data()")
        # Alternatively, if the stored procedure returns a result set, you can use fetch:
        # result = await conn.fetch(f"SELECT * FROM {procedure_name}({', '.join(str(arg) for arg in args)})")
        return result
    except asyncpg.exceptions.PostgresError as e:
        # Handle any exceptions
        print(f"Error executing stored procedure: {e}")
        return None