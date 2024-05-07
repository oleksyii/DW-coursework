import psycopg2
import ast

def read_data(filename='steam_games.txt'):
    data = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i >= 50000:
                break
            try:
                parsed_line = ast.literal_eval(line)
                if 'genres' in parsed_line and 'publisher' in parsed_line and 'developer'  and 'id' in parsed_line:
                    data.append(parsed_line)
            except UnicodeDecodeError:
                    print(f"Skipping line {line} due to UnicodeDecodeError")
                    continue
            except ValueError:
                    print(f"Skipping line {line} due to ValueError")
                    continue
    result = {}
    for row in data:
        temp = []
        for g in row['genres']:
            temp.append(g)
        result[row['id']] = temp
    
    return result

def insert_game_genres(data):
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

    # Insert data into the publisher table
    for key in data.keys():
        genres = ""
        for genre in data[key]:
            genres += genre + ','
        genres = genres[:-1]
        cur.execute("CALL insert_game_genre(%s, %s);", (key, genres))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()
    print('\n\nINSERT WAS SUCCESFULL, I hope')