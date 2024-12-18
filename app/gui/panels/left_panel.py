from tkinter import *
from tkinter import simpledialog, filedialog, messagebox
from app.func.add_song import add_song
from app.func.utils import fetch_playlists
from app.db.db_operations import insert_song
from app.func.add_playlist import create_empty_playlist, import_playlist_from_folder
from app.func.playlist_utils import update_playlist_buttons, change_playlist_cover
from app.func.playlist_handler import delete_playlist



def create_left_panel(parent):
    left_frame = Frame(parent, bg='#1E052A', borderwidth=0)
    left_frame.grid(row=1, column=0, sticky='nsew')

    buttons_frame = Frame(left_frame, bg='#2d0232')
    buttons_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    playlist_frame = Frame(left_frame, bg='#2d0232')
    playlist_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

    Button(
        buttons_frame,
        text="Add Song",
        font=("Arial", 12),
        command=lambda: add_song_with_playlist(),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0
    ).pack(fill="x", padx=10, pady=5)

    Button(
        buttons_frame,
        text="Create Playlist",
        font=("Arial", 12),
        command=lambda: create_empty_playlist(playlist_frame),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0
    ).pack(fill="x", padx=10, pady=5)
    
    Button(
        buttons_frame,
        text="Import playlist",
        font=("Arial", 12),
        command=lambda: import_playlist_from_folder(playlist_frame),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0
    ).pack(fill="x", padx=10, pady=5)


    Button(
        buttons_frame,
        text="Analyze Song",
        font=("Arial", 12),
        # command=lambda: create_playlist_prompt(),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        padx=10, pady=5
    ).pack(fill="x", padx=10, pady=5)

    update_playlist_buttons(playlist_frame, delete_playlist, change_playlist_cover)

    return left_frame




def add_song_with_playlist():
    playlists = fetch_playlists()
    if not playlists:
        messagebox.showwarning("Warning", "No playlists available. Add a playlist first.")
        return

    selected_playlist = simpledialog.askstring("Select Playlist", f"Choose playlist:\n{', '.join(playlists)}")
    if selected_playlist:
        file_path = filedialog.askopenfilename(
            title="Select a music file",
            filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")]
        )
        if file_path:
            add_song(file_path, selected_playlist)
            messagebox.showinfo("Success", f"Song added to playlist '{selected_playlist}'.")
        else:
            messagebox.showinfo("Info", "No file selected.")


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
