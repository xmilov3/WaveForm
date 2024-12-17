import os
from app.db.db_operations import insert_song
from app.func.utils import process_playlist_from_folder
from app.db.database import create_connection

def add_song(file_path, playlist_name):
    connection = create_connection()
    if not connection:
        print("Failed to connect to database.")
        return

    try:
        title = os.path.basename(file_path).split('.')[0]
        insert_song(connection, user_id=1, title=title, artist="Unknown Artist",
                    album=playlist_name, genre="Unknown Genre",
                    file_path=file_path, cover_path="app/gui/assets/covers/song_covers/song_cover.png")
        print(f"Song '{title}' added to playlist '{playlist_name}'.")
    except Exception as e:
        print(f"Error adding song: {e}")
    finally:
        connection.close()
