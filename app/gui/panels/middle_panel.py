from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
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
        return details
    except mysql.connector.Error as e:
        print(f"Error while fetching playlist details: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def fetch_songs_by_playlist(playlist_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()
        cursor.execute("SELECT playlist_id FROM playlists WHERE name = %s", (playlist_name,))
        playlist = cursor.fetchone()
        if not playlist:
            return []

        playlist_id = playlist[0]
        query = """
            SELECT s.title, s.artist
            FROM songs s
            JOIN playlist_songs ps ON s.song_id = ps.song_id
            WHERE ps.playlist_id = %s
        """
        cursor.execute(query, (playlist_id,))
        songs = cursor.fetchall()
        return songs
    except mysql.connector.Error as e:
        print(f"Error while fetching songs: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update_header(header_label, header_image_label, user_label, song_count_label, playlist_name):
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
            header_image_label.config(image="")
    else:
        header_label.config(text="Unknown Playlist")
        user_label.config(text="Unknown Author")
        song_count_label.config(text="0 songs")
        header_image_label.config(image="")




def update_song_listbox(song_listbox, playlist_name):
    songs = fetch_songs_by_playlist(playlist_name)
    song_listbox.delete(0, tk.END)
    if not songs:
        song_listbox.insert(tk.END, "No songs found.")
    else:
        for song in songs:
            title, artist = song
            song_listbox.insert(tk.END, f"{title} - {artist}")



def create_middle_panel(parent, playlist_name):
    middle_frame = tk.Frame(parent, bg="#1E052A")
    song_listbox = Listbox(middle_frame, bg="#2D0232")
    middle_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    header_frame = tk.Frame(middle_frame, bg="#2D0232")
    header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

    header_image_label = tk.Label(header_frame, bg="#2D0232")
    header_image_label.grid(row=0, column=0, rowspan=3, padx=5, pady=5, sticky="nw")

    header_label = tk.Label(header_frame, text="", font=("Arial", 36, "bold"), fg="gray", bg="#2D0232")
    header_label.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))

    user_label = tk.Label(header_frame, text="", font=("Arial", 20), fg="gray", bg="#2D0232")
    user_label.grid(row=1, column=1, sticky="w", padx=(10, 0))

    song_count_label = tk.Label(header_frame, text="", font=("Arial", 16), fg="white", bg="#2D0232")
    song_count_label.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(0, 5))

    songlist_frame = tk.Frame(middle_frame, bg="#1E052A")
    songlist_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    song_listbox = tk.Listbox(
        songlist_frame,
        bg="#2D0232",
        font=("Arial", 16),
        selectbackground="#50184A",
        selectforeground="white",
        borderwidth=0,
        highlightthickness=0,
        fg="white"
    )
    song_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    middle_frame.grid_rowconfigure(0, weight=0)
    middle_frame.grid_rowconfigure(1, weight=1)
    middle_frame.grid_columnconfigure(0, weight=1)

    update_header(header_label, header_image_label, user_label, song_count_label, playlist_name)
    update_song_listbox(song_listbox, playlist_name)

    return middle_frame, song_listbox

