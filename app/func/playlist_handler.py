import os
import mysql.connector
from app.db.database import create_connection
from tkinter import simpledialog, filedialog, messagebox
from app.db.db_operations import insert_song


def get_playlist_id_if_exists(connection, playlist_name):
    try:
        cursor = connection.cursor()
        query = "SELECT playlist_id FROM playlists WHERE name = %s"
        cursor.execute(query, (playlist_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except mysql.connector.Error as e:
        print(f"Error while checking playlist existence: {e}")
        return None
    finally:
        cursor.close()


def create_playlist(playlist_name, folder_path, insert_song_function):
    connection = create_connection()
    if not connection:
        raise Exception("Failed to connect to database.")

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO playlists (user_id, name, description, created_at, created_by)
            VALUES (%s, %s, %s, NOW(), %s);
        """
        cursor.execute(query, (1, playlist_name, "User-created playlist", "system"))
        connection.commit()
        playlist_id = cursor.lastrowid

        for file in os.listdir(folder_path):
            if file.endswith(('.mp3', '.wav')):
                file_path = os.path.join(folder_path, file)
                title = os.path.splitext(file)[0]
                insert_song_function(connection, user_id=1, title=title, artist="Unknown Artist",
                                     album=playlist_name, genre="Unknown Genre",
                                     file_path=file_path, cover_path="/path/to/default_cover.png")
        
        print(f"Playlist '{playlist_name}' created with ID: {playlist_id}")
    except Exception as e:
        print(f"Error while creating playlist: {e}")
        raise
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def fetch_playlists():
    from app.db.database import create_connection

    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM playlists")
        playlists = [row[0] for row in cursor.fetchall()]
        return playlists
    except Exception as e:
        print(f"Error fetching playlists: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

            
def load_playlist_songs(playlist_name):
    from app.db.database import create_connection

    print(f"Loading songs for playlist: {playlist_name}")
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
            SELECT songs.title, songs.artist
            FROM songs
            JOIN playlist_songs ON songs.song_id = playlist_songs.song_id
            JOIN playlists ON playlists.playlist_id = playlist_songs.playlist_id
            WHERE playlists.name = %s
        """
        cursor.execute(query, (playlist_name,))
        songs = cursor.fetchall()
        print(f"Fetched songs: {songs}")

        if songs:
            print(f"Songs in '{playlist_name}':")
            for song in songs:
                print(f"Title: {song[0]}, Artist: {song[1]}")
        else:
            print(f"No songs found in playlist '{playlist_name}'.")

    except Exception as e:
        print(f"Error loading songs: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
