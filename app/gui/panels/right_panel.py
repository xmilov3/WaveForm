from tkinter import Frame, Label, Listbox
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
            SELECT s.title, s.artist, p.name, s.cover_path
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
            SELECT s.title, s.artist
            FROM songs s
            JOIN playlist_songs ps ON s.song_id = ps.song_id
            JOIN playlists p ON ps.playlist_id = p.playlist_id
            WHERE p.name = %s
            LIMIT 10 OFFSET 1
        """
        cursor.execute(query, (playlist_name,))
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


def create_right_panel(parent, playlist_name="Liked Songs"):
    right_frame = Frame(parent, bg='#1E052A', borderwidth=0, highlightbackground='#845162', highlightthickness=0)
    right_frame.grid(row=1, column=2, sticky='nsew', padx=0, pady=0)  # Matching padding for consistency

    parent.grid_rowconfigure(1, weight=1)
    parent.grid_columnconfigure(2, weight=4)

    now_playing_frame = Frame(right_frame, bg='#2d0232', borderwidth=0, highlightbackground='#845162', highlightthickness=2)
    now_playing_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=(30, 30))  # Consistent top padding with space below

    playlist_label = Label(
        now_playing_frame,
        text="Liked Songs",
        font=("Arial", 30, "bold"),
        fg='white',
        bg='#2d0232',
        anchor="w"
    )
    playlist_label.pack(fill="both", expand=True, padx=10, pady=(10, 40))

    album_art_label = Label(
        now_playing_frame,
        bg='#2d0232',
        borderwidth=0,
        highlightthickness=0
    )
    album_art_label.pack(fill="x", padx=10, pady=(10, 5), expand=True)

    title_label = Label(
        now_playing_frame,
        fg="white",
        bg='#2d0232',
        font=("Arial", 14, "bold"),
        anchor="w"
    )
    title_label.pack(fill="x", padx=10, pady=(5, 0))

    artist_label = Label(
        now_playing_frame,
        fg="gray",
        bg='#2d0232',
        font=("Arial", 16),
        anchor="w"
    )
    artist_label.pack(fill="x", padx=10, pady=(0, 10))

    next_in_queue_frame = Frame(right_frame, bg='#2d0232', borderwidth=0, highlightbackground='#845162', highlightthickness=2)
    next_in_queue_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 60))  # Space above and consistent bottom padding

    queue_label = Label(
        next_in_queue_frame,
        text="Next in Queue",
        font=("Arial", 14, "bold"),
        fg='white',
        bg='#2d0232',
        anchor="w"
    )
    queue_label.pack(fill="both", expand=True, padx=10, pady=(0, 40))

    queue_listbox = Listbox(
        next_in_queue_frame,
        bg='#2d0232',
        font=("Arial", 16),
        selectbackground="#50184A",
        selectforeground="white",
        borderwidth=0,
        highlightthickness=0,
        fg="white"
    )
    queue_listbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    update_now_playing(
        playlist_label=playlist_label,
        album_art_label=album_art_label,
        title_label=title_label,
        artist_label=artist_label,
        playlist_name=playlist_name
    )

    update_next_in_queue(queue_listbox, playlist_name)

    right_frame.grid_rowconfigure(0, weight=4)
    right_frame.grid_rowconfigure(1, weight=8)
    right_frame.grid_columnconfigure(0, weight=1)

    return right_frame






def update_now_playing(playlist_label, album_art_label, title_label, artist_label, playlist_name):
    print(f"Updating now playing for playlist: {playlist_name}")
    song_details = fetch_current_song_details(playlist_name)

    if song_details:
        title, artist, playlist, cover_path = song_details

        playlist_label.config(text=playlist)
        title_label.config(text=title)
        artist_label.config(text=artist)

        if cover_path and os.path.exists(cover_path):
            try:
                img = Image.open(cover_path)
                img = img.resize((200, 200), Image.LANCZOS)
                album_image = ImageTk.PhotoImage(img)
                album_art_label.config(image=album_image)
                album_art_label.image = album_image
            except Exception as e:
                print(f"Error loading album art image: {e}")
                album_art_label.config(image='', text="No Cover")
        else:
            print("Invalid or missing cover path.")
            album_art_label.config(image='', text="No Cover")
    else:
        playlist_label.config(text="Unknown Playlist")
        title_label.config(text="No Song")
        artist_label.config(text="Unknown Artist")
        album_art_label.config(image='', text="No Cover")


def update_next_in_queue(queue_listbox, playlist_name):
    print(f"Updating next in queue for playlist: {playlist_name}")
    next_songs = fetch_next_in_queue(playlist_name)

    queue_listbox.delete(0, 'end')
    if next_songs:
        for song in next_songs:
            title, artist = song
            queue_listbox.insert('end', f"{title} - {artist}")
    else:
        queue_listbox.insert('end', "No songs in queue.")
