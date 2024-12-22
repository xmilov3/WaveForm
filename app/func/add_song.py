import os
from app.db.db_operations import insert_song
from app.db.database import create_connection
from app.db.song_operations import insert_song
from app.func.playlist_handler import create_playlist, delete_playlist
from tkinter import messagebox, simpledialog, filedialog
from app.func.playlist_utils import fetch_playlists


def add_song_with_playlist(page_manager):
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


def add_song(file_path, playlist_name):
    connection = create_connection()
    if not connection:
        print("Failed to connect to database.")
        return

    try:
        title = os.path.basename(file_path).split('.')[0]
        insert_song(connection, user_id=1, title=title, artist="Unknown Artist",
                    album=playlist_name, genre="Unknown Genre",
                    file_path=file_path, cover_path="app/gui/assets/covers/song_covers/song_cover.png")
        print(f"Song '{title}' added to playlist '{playlist_name}'.")
    except Exception as e:
        print(f"Error adding song: {e}")
    finally:
        connection.close()
