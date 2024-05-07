import os
import psycopg2
import ast
from faker import Faker

def read_data(filename='steam_games.txt'):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 50000:
                break
            try:
                parsed_line = ast.literal_eval(line)
                if 'user_id' in parsed_line and 'items' in parsed_line:
                    data.append(parsed_line)
                
                if i == 0: print(f"First Line: {parsed_line}")
            except UnicodeDecodeError:
                    print(f"Skipping line {line} due to UnicodeDecodeError")
                    continue
            except ValueError:
                    print(f"Skipping line {line} due to ValueError")
                    continue
    result = {}
    for row in data:
        temp = []
        for g in row['items']:
            temp.append(g['item_id'])
        result[row['user_id']] = temp
    
    return result

def insert_publishers_developers(data):
    # Establish connection to the database
    conn = psycopg2.connect(
        dbname="oltp_dw",
        user="postgres",
        password="alex235689",
        host="localhost",
        port="5432"
    )

    # Create a cursor object
    cur = conn.cursor()
    print("connection established")
    # Insert data into the publisher table
    for key, index in data.keys():
        cur.execute("SELECT user_id FROM \"user\" WHERE user_id_string = %s", (key,))
        actual_user_id = cur.fetchone()[0]
      
        # Convert the games string to a list of integers
        game_ids = [int(game) for game in data[key]]
        # Create a placeholder for the same number of elements as the game_ids list
        placeholders = ','.join(['%s'] * len(game_ids))
        # Execute the SQL query with the list of game_ids
        cur.execute("SELECT game_id FROM game WHERE app_id IN ({})".format(placeholders), game_ids)
        # Fetch the actual game IDs
        actual_game_ids = cur.fetchall()

        for game in actual_game_ids:
            cur.execute("INSERT INTO user_game (user_id, game_id) VALUES (%s, %s)", (actual_user_id, game))
        
        if index == 0:
            print(f"First insert: {actual_user_id}, {game}")

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()
    print('\n\nINSERT WAS SUCCESFULL, I hope')

def insert_user_games(data):
    conn = psycopg2.connect(
        dbname="oltp_dw",
        user="postgres",
        password="alex235689",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()
    
    try:
        for key, game_ids in data.items():
            if not game_ids:  # Skip empty game lists
                continue
            
            cur.execute("SELECT user_id FROM \"user\" WHERE user_id_string = %s", (key,))
            actual_user_id = cur.fetchone()
            if actual_user_id:
                actual_user_id = actual_user_id[0]
                cur.execute("SELECT game_id FROM game WHERE app_id IN %s", (tuple(game_ids),))
                actual_game_ids = cur.fetchall()
                if actual_game_ids:
                    user_game_values = [(actual_user_id, game[0]) for game in actual_game_ids]
                    cur.executemany("INSERT INTO user_game (user_id, game_id) VALUES (%s, %s)", user_game_values)

        conn.commit()
        print('\n\nINSERT WAS SUCCESSFUL')
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        cur.close()
        conn.close()
