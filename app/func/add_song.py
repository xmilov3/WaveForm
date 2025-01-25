import os
from app.db.db_operations import insert_song
from app.db.database import create_connection
import mysql.connector
from app.db.song_operations import insert_song
from app.func.playlist_handler import create_playlist, delete_playlist
from tkinter import messagebox, simpledialog, filedialog, END
from app.func.playlist_utils import fetch_playlists
from tkinter import Toplevel, Label, Listbox, Scrollbar, Button, filedialog, messagebox
from app.func.session import user_session
import re

def add_song_to_playlist(file_path, playlist_name):
    connection = create_connection()
    if not connection:
        print("Failed to connect to database.")
        return
        
    if not user_session.user_id:
        print("No user logged in.")
        messagebox.showerror("Error", "You must be logged in to add songs.")
        return

    try:
        title_artist = os.path.basename(file_path).split('.')[0]
        match = re.match(r"(.*?)\s*-\s*(.*)", title_artist)
        if match:
            artist = match.group(1).strip()
            title = match.group(2).strip()
        else:
            artist = "Unknown Artist" 
            title = title_artist.strip()

        cursor = connection.cursor()
        
        check_user_query = "SELECT user_id FROM users WHERE user_id = %s"
        cursor.execute(check_user_query, (user_session.user_id,))
        if not cursor.fetchone():
            raise Exception(f"User with ID {user_session.user_id} does not exist")

        insert_song_query = """
            INSERT INTO songs (user_id, title, artist, album, genre, file_path, cover_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_song_query, (
            user_session.user_id,
            title,
            artist,
            playlist_name,
            "Unknown Genre",
            file_path,
            "/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm_newest_copy/app/gui/assets/covers/playlist_covers/default_cover.png"
        ))
        connection.commit()

        song_id = cursor.lastrowid

        get_playlist_id_query = "SELECT playlist_id FROM playlists WHERE name = %s"
        cursor.execute(get_playlist_id_query, (playlist_name,))
        result = cursor.fetchone()
        if not result:
            raise Exception(f"Playlist '{playlist_name}' not found in the database.")
        playlist_id = result[0]

        insert_playlist_song_query = """
            INSERT INTO playlist_songs (playlist_id, song_id)
            VALUES (%s, %s)
        """
        cursor.execute(insert_playlist_song_query, (playlist_id, song_id))
        connection.commit()

        playlist_songs_id = cursor.lastrowid

        print(f"Song '{title}' by '{artist}' added to playlist '{playlist_name}'.")
        print(f"playlist_songs_id: {playlist_songs_id}, playlist_id: {playlist_id}, song_id: {song_id}")

    except Exception as e:
        print(f"Error adding song: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def add_song_dialog(playlist_name, song_listbox):
    if not playlist_name:
        messagebox.showwarning("Warning", "No playlist selected.")
        return

    file_path = filedialog.askopenfilename(
        title="Select a music file",
        filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")]
    )

    if file_path:
        try:
            add_song_to_playlist(file_path, playlist_name)
            refresh_song_listbox(song_listbox, playlist_name)
            song_listbox.update_idletasks()
            messagebox.showinfo("Success", f"Song added to playlist '{playlist_name}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add song: {e}")
    else:
        messagebox.showinfo("Info", "No file selected.")

def refresh_song_listbox(song_listbox, playlist_name):
    try:
        connection = create_connection()
        if not connection:
            print("Failed to connect to database.")
            return

        cursor = connection.cursor()
        query = """
            SELECT s.title, s.artist
            FROM songs s
            JOIN playlist_songs ps ON s.song_id = ps.song_id
            JOIN playlists p ON ps.playlist_id = p.playlist_id
            WHERE p.name = %s
            ORDER BY ps.song_id ASC
        """
        cursor.execute(query, (playlist_name,))
        songs = cursor.fetchall()

        song_listbox.delete(0, END)

        for title, artist in songs:
            song_listbox.insert(END, f"{title} - {artist}")

        if not songs:
            print(f"No songs found for playlist '{playlist_name}'.")

    except mysql.connector.Error as e:
        print(f"Database error while refreshing song listbox: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
