
from pydantic import BaseModel


USERS = ["1122305938"]

class User(BaseModel):
    username: str

async def registerActiveUser(username):
    """Registers a user in a list of active users

    Args:
        username (String): The username to be registered

    Returns:
        Integer: The index of a user registered (could be replaced by some kind of token, but I`m lazy)
    """
    USERS.append(username)
    return USERS.index(username) 


async def getUserByIndex(index):
    return USERS[index]

async def getUserData(conn, user_id):
    query = '''
    SELECT
        c.name as country
    FROM country c
    '''
    countries = await conn.fetch(query)
    return countries    