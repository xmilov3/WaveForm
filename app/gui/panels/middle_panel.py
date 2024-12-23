from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
from app.func.playlist_utils import fetch_playlists
import tkinter as tk



def fetch_playlist_details(playlist_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()
        query = """
            SELECT p.name, p.description, p.playlist_cover_path, p.created_by, COUNT(ps.song_id)
            FROM playlists p
            LEFT JOIN playlist_songs ps ON p.playlist_id = ps.playlist_id
            WHERE p.name = %s
            GROUP BY p.playlist_id
        """
        cursor.execute(query, (playlist_name,))
        details = cursor.fetchone()
        if not details:
            return ("Unknown Playlist", "", "", "Unknown Author", 0)
        return details
    except mysql.connector.Error as e:
        print(f"Error while fetching playlist details: {e}")
        return ("Unknown Playlist", "", "", "Unknown Author", 0)
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()




def create_header_frame(parent, playlist_name=None):
    header_frame = Frame(parent, bg="#2D0232")

    header_image_label = Label(header_frame, bg="#2D0232")
    header_image_label.grid(row=0, column=0, rowspan=3, padx=5, pady=5, sticky="nw")

    header_label = Label(header_frame, text="", font=("Arial", 36, "bold"), fg="gray", bg="#2D0232")
    header_label.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))

    user_label = Label(header_frame, text="", font=("Arial", 20), fg="gray", bg="#2D0232")
    user_label.grid(row=1, column=1, sticky="w", padx=(10, 0))

    song_count_label = Label(header_frame, text="", font=("Arial", 16), fg="white", bg="#2D0232")
    song_count_label.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(0, 5))

    details = fetch_playlist_details(playlist_name)
    if details:
        name, description, cover_path, created_by, song_count = details
        header_label.config(text=name)
        user_label.config(text=f"By {created_by if created_by else 'Unknown User'}")
        song_count_label.config(text=f"{song_count} songs")
        if cover_path:
            try:
                img = Image.open(cover_path)
                img = img.resize((150, 150), Image.LANCZOS)
                cover_image = ImageTk.PhotoImage(img)
                header_image_label.config(image=cover_image)
                header_image_label.image = cover_image
            except Exception as e:
                print(f"Error loading cover image: {e}")
                header_image_label.config(image="")
    else:
        header_label.config(text="Unknown Playlist")
        user_label.config(text="Unknown Author")
        song_count_label.config(text="0 songs")
        header_image_label.config(image="")

    return header_frame


def create_song_listbox(parent, playlist_name):
    song_listbox = Listbox(
        parent,
        bg='#2D0232',
        fg='grey',
        selectforeground='grey',
        font=("Arial", 14),
        relief="flat"
    )
    song_listbox.grid(sticky="nsew", padx=5, pady=5)

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

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
            ORDER BY ps.song_id ASC
        """
        cursor.execute(query, (playlist_name,))
        songs = cursor.fetchall()

        for song in songs:
            title, artist = song
            song_listbox.insert(END, f"{title} - {artist}")

        if not songs:
            print(f"No songs found in playlist: {playlist_name}")

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

    return song_listbox




def create_middle_panel(parent, playlist_name):
    middle_frame = Frame(parent, bg="#1E052A", width=600, height=400)
    middle_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    middle_frame.grid_propagate(False)

    header_frame = create_header_frame(middle_frame, playlist_name)
    header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    songlist_frame = Frame(middle_frame, bg="#2D0232")
    songlist_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    song_listbox = create_song_listbox(songlist_frame, playlist_name)

    middle_frame.grid_rowconfigure(0, weight=0)
    middle_frame.grid_rowconfigure(1, weight=1)
    middle_frame.grid_columnconfigure(0, weight=1)

    return middle_frame, header_frame, songlist_frame, song_listbox

