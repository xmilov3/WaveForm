import os
import mysql.connector
from app.db.database import create_connection

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

def create_playlist(user_id, folder_path, insert_song_function):
    connection = create_connection()
    if not connection:
        print("Failed to connect to database.")
        return

    playlist_name = os.path.basename(folder_path)
    playlist_cover_path = os.path.join(folder_path, "cover", "cover.png")

    playlist_id = get_playlist_id_if_exists(connection, playlist_name)
    if not playlist_id:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO playlists (user_id, name, description, created_by, playlist_cover_path)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, playlist_name, "User-created playlist", user_id, playlist_cover_path))
            connection.commit()
            playlist_id = cursor.lastrowid
            print(f"Playlist '{playlist_name}' created with ID: {playlist_id}.")
        except mysql.connector.Error as e:
            print(f"Error while creating playlist: {e}")
            return
        finally:
            cursor.close()

    for file in os.listdir(folder_path):
        if file.lower().endswith(('.mp3', '.wav')):
            file_path = os.path.join(folder_path, file)
            title, _ = os.path.splitext(file)

            try:
                insert_song_function(connection, user_id, title, "Unknown Artist", playlist_name, "Unknown Genre", file_path, playlist_cover_path)
                print(f"Added song '{title}' to database.")
            except mysql.connector.Error as e:
                print(f"Error while inserting song: {e}")
                continue

    connection.close()
    print(f"Playlist '{playlist_name}' successfully created/updated.")

def fetch_playlists():
    connection = create_connection()
    if not connection:
        print("Failed to connect to database.")
        return []

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM playlists")
        playlists = cursor.fetchall()
        return [playlist[0] for playlist in playlists]
    except Exception as e:
        print(f"Error while fetching playlists: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()