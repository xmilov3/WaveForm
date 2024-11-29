import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


load_dotenv()

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error while connecting to database: {e}")
        return None

def insert_song(connection, user_id, title, artist, album, genre, file_path, cover_path):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO songs (user_id, title, artist, album, genre, file_path, cover_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        values = (user_id, title, artist, album, genre, file_path, cover_path)
        cursor.execute(query, values)
        connection.commit()
        print("Record inserted successfully into songs table.")
    except Error as e:
        print(f"Error while inserting song: {e}")
    finally:
        cursor.close()