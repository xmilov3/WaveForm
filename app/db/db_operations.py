import mysql.connector
from app.func.session import user_session


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
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(f"Error while inserting song: {e}")
        return None
    finally:
        cursor.close()

