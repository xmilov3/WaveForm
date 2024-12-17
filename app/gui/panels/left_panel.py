from tkinter import *
from tkinter import simpledialog, filedialog, messagebox
from app.func.add_song import add_song
from app.func.utils import fetch_playlists
from app.db.db_operations import insert_song
from app.func.playlist_handler import create_playlist

def create_left_panel(parent):
    left_frame = Frame(parent, bg='#1E052A', borderwidth=0, highlightbackground='#845162', highlightthickness=0)
    left_frame.grid(row=1, column=0, sticky='nsew', padx=0, pady=0)

    buttons_frame = Frame(left_frame, bg='#2d0232', borderwidth=0, highlightbackground='#845162', highlightthickness=2)
    buttons_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    add_song_button = Button(
        buttons_frame,
        text="Add Song",
        font=("Arial", 12),
        command=lambda: add_song_with_playlist(),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        padx=10, pady=5
    )
    add_song_button.pack(fill="x", padx=10, pady=5)

    add_playlist_button = Button(
        buttons_frame,
        text="Add Playlist",
        font=("Arial", 12),
        command=lambda: create_playlist_prompt(playlist_frame),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        padx=10, pady=5
    )
    add_playlist_button.pack(fill="x", padx=10, pady=5)

    create_playlist_button = Button(
        buttons_frame,
        text="Create Playlist",
        font=("Arial", 12),
        # command=lambda: add_playlist_prompt(),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        padx=10, pady=5
    )
    create_playlist_button.pack(fill="x", padx=10, pady=5)


    analyze_song_button = Button(
        buttons_frame,
        text="Analyze Song",
        font=("Arial", 12),
        command=lambda: create_playlist_prompt(),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        padx=10, pady=5
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
            padx=10, pady=5,
            command=lambda name=playlist_name: on_playlist_click(name)
        )
        playlist_button.pack(fill="x", padx=10, pady=5)

def add_song_with_playlist():
    playlists = fetch_playlists()
    if not playlists:
        messagebox.showwarning("Warning", "No playlists available. Add a playlist first.")
        return

    selected_playlist = simpledialog.askstring("Select Playlist", f"Choose playlist:\n{', '.join(playlists)}")
    if selected_playlist:
        file_path = filedialog.askopenfilename(
            title="Select a music file",
            filetypes=(("MP3 Files", "*.mp3"), ("WAV Files", "*.wav"))
        )
        if file_path:
            add_song(file_path, selected_playlist)
            messagebox.showinfo("Success", f"Song added to playlist '{selected_playlist}'.")
        else:
            messagebox.showinfo("Info", "No file selected.")

def create_playlist_prompt(playlist_frame):
    from app.func.playlist_handler import create_playlist
    from app.func.utils import insert_song

    playlist_name = simpledialog.askstring("Create Playlist", "Enter new playlist name:")
    if not playlist_name:
        messagebox.showwarning("Warning", "Playlist name cannot be empty!")
        return

    folder_path = filedialog.askdirectory(title="Select Folder for Playlist")
    if not folder_path:
        messagebox.showwarning("Warning", "No folder selected!")
        return

    try:
        create_playlist(playlist_name, folder_path, insert_song)
        messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully!")
        
        update_playlist_buttons(playlist_frame)
    except Exception as e:
        print(f"Error creating playlist: {e}")
        messagebox.showerror("Error", f"Failed to create playlist: {e}")


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
