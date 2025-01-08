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
    right_frame = Frame(parent, bg='#1E052A', width=300)
    right_frame.grid(row=1, column=2, sticky='nsew')
    right_frame.grid_propagate(False)

    right_frame.grid_rowconfigure(0, weight=2)  # Now Playing Frame
    right_frame.grid_rowconfigure(1, weight=1)  # Queue frame
    right_frame.grid_columnconfigure(0, weight=1)

    now_playing_frame = Frame(right_frame, bg='#2d0232')
    now_playing_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
   
    now_playing_frame.grid_rowconfigure(0, weight=0)
    now_playing_frame.grid_rowconfigure(1, weight=2)
    now_playing_frame.grid_rowconfigure(2, weight=0)
    now_playing_frame.grid_rowconfigure(3, weight=0)
    now_playing_frame.grid_columnconfigure(0, weight=1)

    playlist_label = Label(now_playing_frame, text="Now Playing", font=("Arial", 30, "bold"), fg='white', bg='#2d0232')
    playlist_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=2)

    album_art_label = Label(now_playing_frame, bg='#2d0232')
    album_art_label.grid(row=1, column=0, sticky='nsew', padx=5, pady=2)

    title_label = Label(now_playing_frame, fg="white", bg='#2d0232', font=("Arial", 14, "bold"))
    title_label.grid(row=2, column=0, sticky='nsew', padx=5, pady=2)

    artist_label = Label(now_playing_frame, fg="gray", bg='#2d0232', font=("Arial", 16))
    artist_label.grid(row=3, column=0, sticky='nsew', padx=5, pady=2)

    next_in_queue_frame = Frame(right_frame, bg='#2d0232')
    next_in_queue_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

    next_in_queue_frame.grid_rowconfigure(0, weight=0)  # Queue label
    next_in_queue_frame.grid_rowconfigure(1, weight=1)  # Queue content
    next_in_queue_frame.grid_columnconfigure(0, weight=1)

    queue_label = Label(next_in_queue_frame, text="Next in Queue", font=("Arial", 14, "bold"), fg='white', bg='#2d0232')
    queue_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    queue_text_label = Label(next_in_queue_frame, bg='#2d0232', fg="white", font=("Arial", 12))
    queue_text_label.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

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
                        img = img.resize((300, 300), Image.LANCZOS)
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



def update_next_in_queue(queue_text_label, playlist_name):
    if queue_text_label is None:
        print("Error: queue_text_label is None")
        return

    print(f"Updating next in queue for playlist: {playlist_name}")
    next_songs = fetch_next_in_queue(playlist_name)

    if next_songs:
        queue_text = "\n".join([f"{title} - {artist}" for title, artist in next_songs])
    else:
        queue_text = "No songs in queue."

    queue_text_label.config(text=queue_text)
