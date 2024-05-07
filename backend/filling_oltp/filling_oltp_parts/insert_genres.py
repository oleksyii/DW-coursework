import psycopg2
import ast
from faker import Faker

def read_data(filename='steam_games.txt'):
    data = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i >= 50000:
                break
            try:
                parsed_line = ast.literal_eval(line)
                if 'genres' in parsed_line:
                    data.append(parsed_line)
            except UnicodeDecodeError:
                    print(f"Skipping line {line} due to UnicodeDecodeError")
                    continue
            except ValueError:
                    print(f"Skipping line {line} due to ValueError")
                    continue
    result = set()
    for row in data:
        for g in row['genres']:
            result.add(g)

    return result

def insert_genres(data):
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
    for name in data:
        cur.execute("INSERT INTO genre (name) VALUES (%s)", (name, ))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()
    print('\n\nINSERT WAS SUCCESFULL, I hope')