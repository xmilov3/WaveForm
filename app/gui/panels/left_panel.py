from tkinter import *
from app.func.config import *
from PIL import Image, ImageTk
from app.func.add_song import add_song


def create_left_panel(parent):
    left_frame = Frame(parent, bg='#1E052A', borderwidth=0, highlightbackground='#845162', highlightthickness=0)
    left_frame.grid(row=1, column=0, sticky='nsew', padx=0, pady=0)

    buttons_frame = Frame(left_frame, bg='#2d0232', borderwidth=0, highlightbackground='#845162', highlightthickness=2)
    buttons_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    add_song_button = Button(
        buttons_frame,
        text="Add Song",
        font=("Arial", 12),
        command=lambda: add_song(),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        highlightbackground='#845162',
        highlightthickness=1,
        padx=10,
        pady=5
    )
    add_song_button.pack(fill="x", padx=10, pady=5)

    create_playlist_button = Button(
        buttons_frame,
        text="Create Playlist",
        font=("Arial", 12),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        highlightbackground='#845162',
        highlightthickness=1,
        padx=10,
        pady=5
    )
    create_playlist_button.pack(fill="x", padx=10, pady=5)

    analyze_song_button = Button(
        buttons_frame,
        text="Analyze Song",
        font=("Arial", 12),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        highlightbackground='#845162',
        highlightthickness=1,
        padx=10,
        pady=5
    )
    analyze_song_button.pack(fill="x", padx=10, pady=5)


    playlist_frame = Frame(left_frame, bg='#2d0232', borderwidth=0, highlightbackground='#845162', highlightthickness=2)
    playlist_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

    update_playlist_buttons(playlist_frame)

    return left_frame


def update_playlist_buttons(playlist_frame):
    from app.func.playlist_handler import fetch_playlists

    def on_playlist_click(playlist_name):
        print(f"Playlist clicked: {playlist_name}")
        load_playlist_songs(playlist_name)

    for widget in playlist_frame.winfo_children():
        widget.destroy()

    playlist_label = Label(
        playlist_frame,
        text="Playlists",
        font=("Arial", 14, "bold"),
        fg='#845162',
        bg='#2d0232',
        borderwidth=0,
        anchor="w"
    )
    playlist_label.pack(fill="x", padx=10, pady=10)

    playlists = fetch_playlists()
    for playlist_name in playlists:
        playlist_button = Button(
            playlist_frame,
            text=playlist_name,
            font=("Arial", 12),
            fg='#845162',
            bg='#50184A',
            activebackground='#845162',
            activeforeground='#845162',
            borderwidth=0,
            highlightbackground='#845162',
            highlightthickness=1,
            padx=10,
            pady=5,
            command=lambda name=playlist_name: on_playlist_click(name)
        )
        playlist_button.pack(fill="x", padx=10, pady=5)


def load_playlist_songs(playlist_name):
    from app.db.database import create_connection

    print(f"Loading songs for playlist: {playlist_name}")
    try:
        connection = create_connection()
        if not connection:
            print("Failed to connect to the database.")
            return

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

        if songs:
            print(f"Songs in '{playlist_name}':")
            for song in songs:
                print(f"Title: {song[0]}, Artist: {song[1]}")
        else:
            print(f"No songs found in playlist '{playlist_name}'.")

    except Exception as e:
        print(f"Error loading playlist songs: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
