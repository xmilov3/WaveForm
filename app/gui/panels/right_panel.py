from tkinter import Frame, Label
from PIL import Image, ImageTk
from app.func.config import *
import mysql.connector
import os


def fetch_current_song_details(playlist_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()

        query = """
            SELECT 
                s.title AS song_title, 
                s.artist AS song_artist, 
                s.cover_path AS song_cover_path, 
                p.name AS name, 
                p.cover_path AS playlist_cover_path
            FROM songs s
            JOIN playlist_songs ps ON s.song_id = ps.song_id
            JOIN playlists p ON ps.playlist_id = p.playlist_id
            WHERE p.name = %s
            LIMIT 1
        """
        cursor.execute(query, (playlist_name,))
        song_details = cursor.fetchone()

        if song_details:
            print(f"Current song details fetched: {song_details}")
        else:
            print(f"No song found for playlist: {playlist_name}")

        return song_details
    except mysql.connector.Error as e:
        print(f"Error while fetching current song details: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def fetch_next_in_queue(playlist_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()

        query = """
            SELECT s.title, s.artist, s.cover_path
            FROM songs s
            JOIN playlist_songs ps ON s.song_id = ps.song_id
            JOIN playlists p ON ps.playlist_id = p.playlist_id
            WHERE p.name = %s
            LIMIT 10 OFFSET 1
        """
        cursor.execute(query, (playlist_name))
        queue_songs = cursor.fetchall()

        if queue_songs:
            print(f"Next songs in queue fetched: {queue_songs}")
        else:
            print(f"No next songs found for playlist: {playlist_name}")

        return queue_songs
    except mysql.connector.Error as e:
        print(f"Error while fetching next songs: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def create_right_panel(parent, playlist_name=None):
    right_frame = Frame(parent, bg='#1E052A', borderwidth=0, highlightbackground='#845162', highlightthickness=0, width=300)
    right_frame.grid(row=1, column=2, sticky='nsew')

    right_frame.grid_rowconfigure(0, weight=0) # Now Playing info
    right_frame.grid_rowconfigure(1, weight=1)  # Next in queue
    right_frame.grid_columnconfigure(0, weight=1)

    parent.grid_rowconfigure(1, weight=1)
    parent.grid_columnconfigure(2, weight=0)
    right_frame.grid_propagate(False)

    now_playing_frame = Frame(right_frame, bg='#2d0232', borderwidth=0, highlightbackground='#845162', highlightthickness=2)
    now_playing_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
    now_playing_frame.grid_propagate(False)

    playlist_label = Label(
        now_playing_frame,
        text="Now Playing",
        font=("Arial", 30, "bold"),
        fg='white',
        bg='#2d0232',
        anchor="w"
    )
    playlist_label.pack(fill="both", expand=True, padx=10, pady=(10, 10))

    album_art_label = Label(
        now_playing_frame,
        bg='#2d0232',
        borderwidth=0,
        highlightthickness=0
    )
    album_art_label.pack(fill="x", padx=10, pady=(10, 10), expand=True)

    title_label = Label(
        now_playing_frame,
        fg="white",
        bg='#2d0232',
        font=("Arial", 14, "bold"),
        anchor="w"
    )
    title_label.pack(fill="x", padx=10, pady=(5, 5))

    artist_label = Label(
        now_playing_frame,
        fg="gray",
        bg='#2d0232',
        font=("Arial", 16),
        anchor="w"
    )
    artist_label.pack(fill="x", padx=10, pady=(0, 10))


    next_in_queue_frame = Frame(right_frame, bg='#2d0232', borderwidth=0, highlightbackground='#845162', highlightthickness=2)
    next_in_queue_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
    next_in_queue_frame.grid_columnconfigure(0, weight=1)

    queue_label = Label(
        next_in_queue_frame,
        text="Next in Queue",
        font=("Arial", 14, "bold"),
        fg='white',
        bg='#2d0232',
        anchor="w"
    )
    queue_label.pack(fill="both", expand=True, padx=10, pady=(10, 10))

    queue_text_label = Label(
        next_in_queue_frame,
        text="",
        bg='#2d0232',
        fg="white",
        font=("Arial", 12),
        justify="left",
        anchor="nw"
    )
    queue_text_label.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    return right_frame, queue_text_label, playlist_label, album_art_label, title_label, artist_label

def update_now_playing(playlist_label, album_art_label, title_label, artist_label, playlist_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()

        query = """
            SELECT s.title, s.artist, s.cover_path
            FROM songs s
            JOIN playlist_songs ps ON s.song_id = ps.song_id
            JOIN playlists p ON ps.playlist_id = p.playlist_id
            WHERE p.name = %s
            ORDER BY ps.song_id ASC LIMIT 1
        """
        cursor.execute(query, (playlist_name,))
        song = cursor.fetchone()

        if song:
            song_title, artist_name, cover_path = song
            title_label.config(text=song_title)
            artist_label.config(text=artist_name)

            if album_art_label:
                if cover_path and os.path.exists(cover_path):
                    try:
                        from PIL import Image, ImageTk
                        img = Image.open(cover_path)
                        img = img.resize((200, 200), Image.LANCZOS)
                        album_image = ImageTk.PhotoImage(img)
                        album_art_label.config(image=album_image)
                        album_art_label.image = album_image
                    except Exception as e:
                        print(f"Error loading album art: {e}")
                        album_art_label.config(image='', text="No Cover")
                else:
                    album_art_label.config(image='', text="No Cover")
        else:
            print(f"No songs found in playlist: {playlist_name}")
            title_label.config(text="No Song")
            artist_label.config(text="No Artist")
            if album_art_label:
                album_art_label.config(image='', text="No Cover")

    except mysql.connector.Error as e:
        print(f"Error while fetching current song details: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()



def update_next_in_queue(queue_text_label, playlist_name, current_index=None):
    if not playlist_name:
        print("No playlist name provided to update_next_in_queue.")
        return

    try:
        print(f"Fetching next songs for playlist: {playlist_name}")
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()

        query = """
            SELECT 
                s.title AS song_title,
                s.artist AS song_artist
            FROM songs s
            JOIN playlist_songs ps ON s.song_id = ps.song_id
            JOIN playlists p ON ps.playlist_id = p.playlist_id
            WHERE p.name = %s
        """
        cursor.execute(query, (playlist_name,))
        songs = cursor.fetchall()

        if not songs:
            print(f"No songs found in playlist: {playlist_name}")
            queue_text_label.config(text="No songs in queue.")
            return

        if current_index is not None:
            next_songs = songs[current_index + 1:] + songs[:current_index]
        else:
            next_songs = songs

        display_queue = next_songs[:5]
        queue_text_label.config(text="\n".join(f"{song[0]} - {song[1]}" for song in display_queue))
        print("Next queue updated:", display_queue)

    except Exception as e:
        print(f"Error while fetching next songs: {e}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
