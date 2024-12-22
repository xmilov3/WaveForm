import os
import mysql.connector
from app.db.database import create_connection
from tkinter import Label, messagebox



def process_playlist_from_folder(folder_path, playlist_name, user_id, created_by, insert_song_function, cover_path=None):
    connection = create_connection()
    if not connection:
        print("Cannot connect to database.")
        return None

    playlist_id = None
    try:
        cursor = connection.cursor()

        if not cover_path:
            cover_path = "app/gui/assets/covers/playlist_covers/default_cover.png"

        query = """
            INSERT INTO playlists (user_id, name, description, created_by, playlist_cover_path)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, playlist_name, "Importing playlist", created_by, cover_path))
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
                print(f"Added '{title}' by '{artist}' to '{playlist_name}'")
        return playlist_id
    except Exception as e:
        print(f"Playlist processing error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    return playlist_id


def get_playlist_id_if_exists(connection, playlist_name):
    try:
        cursor = connection.cursor()
        query = "SELECT playlist_id FROM playlists WHERE name = %s"
        cursor.execute(query, (playlist_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error while checking playlist existence: {e}")
        return None
    finally:
        cursor.close()

def create_playlist(user_id, playlist_name, folder_path, insert_song_function):
    connection = create_connection()
    if not connection:
        print("Failed to connect to database.")
        return

    playlist_cover_path = os.path.join(folder_path, "cover", "cover.png")
    playlist_id = None

    try:
        cursor = connection.cursor()
        playlist_id = get_playlist_id_if_exists(connection, playlist_name)
        if not playlist_id:
            query = """
                INSERT INTO playlists (user_id, name, description, created_by, playlist_cover_path)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, playlist_name, "User-created playlist", user_id, playlist_cover_path))
            connection.commit()
            playlist_id = cursor.lastrowid
            print(f"Playlist '{playlist_name}' created with ID: {playlist_id}.")
        else:
            print(f"Playlist '{playlist_name}' already exists with ID: {playlist_id}.")

        for file in os.listdir(folder_path):
            if file.lower().endswith(('.mp3', '.wav')):
                file_path = os.path.join(folder_path, file)
                song_title, artist_name = split_title_and_artist(file)

                insert_song_function(
                    connection,
                    user_id=user_id,
                    title=song_title,
                    artist=artist_name,
                    album=playlist_name,
                    genre="Unknown Genre",
                    file_path=file_path,
                    cover_path=playlist_cover_path
                )
                print(f"Added song '{song_title}' by '{artist_name}' to playlist '{playlist_name}'.")
    except Exception as e:
        print(f"Error creating playlist: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

    print(f"Playlist '{playlist_name}' processing completed.")





def fetch_playlists():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM playlists")
        playlists = [row[0] for row in cursor.fetchall()]
        return playlists
    except Exception as e:
        print(f"Error downloading playlists: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def split_title_and_artist(file_name):
    try:
        base_name = os.path.splitext(file_name)[0]
        parts = base_name.split(" - ", 1)
        if len(parts) == 2:
            artist_name = parts[0].strip()
            song_title = parts[1].strip()
        else:
            artist_name = "Unknown artist"
            song_title = base_name.strip()
        return song_title, artist_name
    except Exception as e:
        print(f"Error while splitting: {e}")
        return "Unknown album", "Unknown artist"
            
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


def delete_playlist(playlist_name, playlist_frame, update_function, page_manager):
    try:
        connection = create_connection()
        if not connection:
            messagebox.showerror("Error", "Failed to connect to the database.")
            return

        cursor = connection.cursor()
        query = "DELETE FROM playlists WHERE name = %s"
        cursor.execute(query, (playlist_name,))
        connection.commit()

        messagebox.showinfo("Success", f"Playlist '{playlist_name}' deleted successfully!")
        update_function(playlist_frame, page_manager)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete playlist: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
