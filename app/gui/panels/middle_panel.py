from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
from app.func.playlist_handler import fetch_playlists
import tkinter as tk
from app.func.music_controller import play_selected_song
from app.func.config import *
from app.func.add_song import add_song_to_playlist, add_song_dialog
from app.func.music_controller import initialize_song_listbox, play_selected_song

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





def display_playlist_details_only(playlist_name, middle_panel, title_label, artist_label, album_art_label, 
                                  time_elapsed_label, time_remaining_label, progress_slider):
    for widget in middle_panel.winfo_children():
        widget.destroy()

    create_middle_panel(
        parent=middle_panel,
        playlist_name=playlist_name,
        title_label=title_label,
        artist_label=artist_label,
        album_art_label=album_art_label,
        time_elapsed_label=time_elapsed_label,
        time_remaining_label=time_remaining_label,
        progress_slider=progress_slider
    )


def create_middle_panel(
    parent, 
    playlist_name, 
    title_label, 
    artist_label,
    album_art_label,
    time_elapsed_label, 
    time_remaining_label,
    progress_slider 
):
    middle_frame = Frame(parent, bg="#1E052A", width=600, height=400)
    middle_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    middle_frame.grid_propagate(False)

    header_frame = create_header_frame(middle_frame, playlist_name)
    header_frame.grid_rowconfigure(3, weight=1)
    add_song_button = Button(
        header_frame,
        text="Add Song to Playlist",
        font=("Arial", 12, "bold"),
        command=lambda: add_song_dialog(playlist_name, song_listbox)
    )
    add_song_button.grid(row=3, column=0, pady=10, sticky="ew")
    header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    songlist_frame = Frame(middle_frame, bg="#2D0232")
    songlist_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    song_listbox = initialize_song_listbox(
        parent=songlist_frame,
        playlist_name=playlist_name,
        album_art_label=album_art_label,
        play_song_callback=play_selected_song,
        title_label=title_label,
        artist_label=artist_label,
        time_elapsed_label=time_elapsed_label,
        time_remaining_label=time_remaining_label,
        progress_slider=progress_slider
    )

    middle_frame.grid_rowconfigure(0, weight=0)
    middle_frame.grid_rowconfigure(1, weight=1)
    middle_frame.grid_columnconfigure(0, weight=1)

    return middle_frame, header_frame, songlist_frame, song_listbox