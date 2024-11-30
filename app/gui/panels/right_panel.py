from tkinter import Frame, Label
from PIL import Image, ImageTk
from app.func.config import *
import mysql.connector

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



def create_right_panel(main_frame, playlist_name="Liked Songs"):
    right_frame = Frame(main_frame, bg='#3A0C60')
    right_frame.grid(row=1, column=2, sticky='nsew', padx=1, pady=1)

    now_playing_frame = Frame(right_frame, bg='#3A0C60')
    now_playing_frame.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
    now_playing_frame.place(relx=0.07, rely=0.26, anchor="w")

    # Label for playlist name
    playlist_right_frame_label = Label(now_playing_frame, text='', font=("Arial", 28, "bold"), anchor="w", fg='white', bg='#3A0C60')
    playlist_right_frame_label.pack(fill="x", pady=25)

    # Label for album art
    album_art_label = Label(now_playing_frame, bg='#3A0C60')
    album_art_label.pack(fill="both", expand=True, pady=2)

    # Label for song title
    title2_label = Label(now_playing_frame, fg="white", bg='#3A0C60', font=("Arial", 20, "bold"), anchor="w")
    title2_label.pack(fill="x", pady=5)

    # Label for song artist
    artist2_label = Label(now_playing_frame, fg="gray", bg='#3A0C60', font=("Arial", 16), anchor="w")
    artist2_label.pack(fill="x")

    # Update content dynamically
    update_now_playing(now_playing_frame, playlist_right_frame_label, album_art_label, title2_label, artist2_label, playlist_name)

    next_in_queue_frame = Frame(right_frame, bg='#3C0F64')
    next_in_queue_frame.grid(row=1, column=0, sticky='nsew', padx=0, pady=1)

    return right_frame

def update_now_playing(frame, playlist_label, album_art_label, title_label, artist_label, playlist_name):
    print(f"Updating now playing for playlist: {playlist_name}")
    song_details = fetch_current_song_details(playlist_name)
    
    if song_details:
        title, artist, playlist, cover_path = song_details
        print(f"Song fetched: Title - {title}, Artist - {artist}, Playlist - {playlist}, Cover - {cover_path}")

        # Update playlist name
        playlist_label.config(text=playlist)

        # Update song title
        title_label.config(text=title)

        # Update song artist
        artist_label.config(text=artist)

        # Update album art
        if cover_path and cover_path.strip():
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
            print("Album art path is empty or invalid.")
            album_art_label.config(image='', text="No Cover")
    else:
        print("No song details found.")
        playlist_label.config(text="Unknown Playlist")
        title_label.config(text="No Song")
        artist_label.config(text="Unknown Artist")
        album_art_label.config(image='', text="No Cover")