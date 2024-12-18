import os
from app.db.database import create_connection


def split_title_and_artist(file_name):
    try:
        base_name = os.path.splitext(file_name)[0]
        parts = base_name.split(" - ", 1)
        if len(parts) == 2:
            artist_name = parts[0].strip()
            song_title = parts[1].strip()
        else:
            artist_name = "Unknown Artist"
            song_title = base_name.strip()
        return song_title, artist_name
    except Exception as e:
        print(f"Error splitting title and artist: {e}")
        return "Unknown Title", "Unknown Artist"

def process_playlist_from_folder(folder_path, playlist_name, user_id, created_by, insert_song_function):
    connection = create_connection()
    if not connection:
        print("Failed to connect to database.")
        return None

    playlist_id = None
    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO playlists (user_id, name, description, created_by, playlist_cover_path)
            VALUES (%s, %s, %s, %s, %s)
        """
        cover_path = "app/gui/assets/covers/default_cover.png"
        cursor.execute(query, (user_id, playlist_name, "Imported playlist", created_by, cover_path))
        connection.commit()
        playlist_id = cursor.lastrowid

        files = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.wav'))]
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            title, artist = split_title_and_artist(file_name)

            song_id = insert_song_function(
                connection,
                user_id=user_id,
                title=title,
                artist=artist,
                album=playlist_name,
                genre="Unknown Genre",
                file_path=file_path,
                cover_path=cover_path
            )

            if song_id:
                cursor.execute(
                    "INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)",
                    (playlist_id, song_id)
                )
                connection.commit()
                print(f"Added song '{title}' by '{artist}' to playlist '{playlist_name}'")
        return playlist_id
    except Exception as e:
        print(f"Error processing playlist: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    return playlist_id

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
