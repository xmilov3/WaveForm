import os
import mysql.connector
from app.db.database import create_connection
from app.db.db_operations import insert_song

def split_title_and_artist(file_name):
    try:
        base_name = os.path.splitext(file_name)[0]
        parts = base_name.split(" - ", 1)
        if len(parts) == 2:
            artist_name = parts[0].strip()
            song_title = parts[1].strip()
        else:
            artist_name = "Unknown Artist"
            song_title = parts[0].strip()

        return song_title, artist_name
    except Exception as e:
        print(f"Error splitting title and artist: {e}")
        return "Unknown Title", "Unknown Artist"

def process_playlist_from_folder(folder_path, user_id, insert_song_function):
    connection = create_connection()
    if not connection:
        print("Failed to connect to database.")
        return

    playlist_name = os.path.basename(folder_path)
    playlist_cover_path = os.path.join(folder_path, "cover", "cover.png")

    print(f"Processing playlist '{playlist_name}' from folder: {folder_path}")

    try:
        for file in os.listdir(folder_path):
            if file.lower().endswith(('.mp3', '.wav')):
                file_path = os.path.join(folder_path, file)
                song_title, artist_name = split_title_and_artist(file)

                cursor = connection.cursor()
                query = """
                    INSERT INTO songs (user_id, title, artist, album, genre, file_path, cover_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (user_id, song_title, artist_name, playlist_name, "Unknown Genre", file_path, playlist_cover_path))
                connection.commit()

                print(f"Added song: '{song_title}' by '{artist_name}'")

        print(f"Playlist '{playlist_name}' successfully created/updated.")
    except Exception as e:
        print(f"Error processing playlist: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()

def fetch_playlists():
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
