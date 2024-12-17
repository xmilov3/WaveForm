import os
from app.db.database import create_connection
from app.db.db_operations import insert_song

def process_playlist_from_folder(folder_path, user_id):
    connection = create_connection()
    if not connection:
        print("Failed to connect to database.")
        return

    playlist_name = os.path.basename(folder_path)
    playlist_cover_path = os.path.join(folder_path, "cover", "cover.png")

    print(f"Processing playlist '{playlist_name}' from folder: {folder_path}")

    for file in os.listdir(folder_path):
        if file.lower().endswith(('.mp3', '.wav')):
            file_path = os.path.join(folder_path, file)
            title, _ = os.path.splitext(file)
            insert_song(connection, user_id, title, "Unknown Artist", playlist_name, "Unknown Genre", file_path, playlist_cover_path)

    connection.close()
    print(f"Playlist '{playlist_name}' successfully created.")

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
