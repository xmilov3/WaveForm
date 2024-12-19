import os
from app.db.database import create_connection
from app.func.session import user_session
from app.func.add_song import insert_song
from tkinter import filedialog, simpledialog, messagebox
from app.func.playlist_handler import create_playlist, delete_playlist
from app.func.playlist_utils import update_playlist_buttons, change_playlist_cover
from app.func.utils import process_playlist_from_folder, split_title_and_artist




def create_empty_playlist(playlist_frame):
    user_id = user_session.user_id
    created_by = user_session.username

    playlist_name = simpledialog.askstring("Create Playlist", "Enter new playlist name:")
    if not playlist_name:
        messagebox.showinfo("Info", "Playlist creation cancelled.")
        return

    cover_path = "app/gui/assets/covers/default_cover.png"

    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO playlists (user_id, name, description, created_by, playlist_cover_path)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, playlist_name, "Empty playlist", created_by, cover_path))
        connection.commit()

        messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully!")
        update_playlist_buttons(playlist_frame, delete_playlist, change_playlist_cover)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to create playlist: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


def import_playlist_from_folder(playlist_frame):
    user_id = user_session.user_id
    created_by = user_session.username

    playlist_name = simpledialog.askstring("Import Playlist", "Enter new playlist name:")
    if not playlist_name:
        messagebox.showinfo("Info", "Playlist creation cancelled.")
        return

    folder_path = filedialog.askdirectory(title="Select Folder with Songs")
    if not folder_path:
        messagebox.showinfo("Info", "No folder selected. Playlist creation cancelled.")
        return

    try:
        print(f"Importing playlist '{playlist_name}' from folder '{folder_path}'")
        playlist_id = process_playlist_from_folder(folder_path, playlist_name, user_id, created_by, insert_song)

        if playlist_id:
            messagebox.showinfo("Success", f"Playlist '{playlist_name}' imported successfully!")
            update_playlist_buttons(playlist_frame, delete_playlist, change_playlist_cover)
        else:
            messagebox.showerror("Error", "Failed to import playlist due to database error.")

    except Exception as e:
        print(f"Error importing playlist: {e}")
        messagebox.showerror("Error", f"Failed to import playlist: {e}")

