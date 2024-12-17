import os
from app.db.database import create_connection
from app.func.add_song import insert_song
from tkinter import filedialog, simpledialog, messagebox
from app.func.playlist_handler import process_playlist_from_folder, process_playlist_from_files
from app.func.utils import process_playlist_from_folder

from app.func.playlist_handler import create_playlist



from tkinter import simpledialog, filedialog, messagebox
from app.func.playlist_handler import create_playlist
from app.db.db_operations import insert_song

from tkinter import simpledialog, filedialog, messagebox
from app.func.playlist_handler import create_playlist
from app.db.db_operations import insert_song

def create_playlist_prompt():
    choice = messagebox.askyesno("Create Playlist", "Do you want to create a playlist from a folder?\n"
                                                   "Yes - Use a folder\nNo - Create an empty playlist.")
    
    playlist_name = simpledialog.askstring("Create Playlist", "Enter new playlist name:")
    if not playlist_name:
        messagebox.showinfo("Info", "Playlist creation cancelled.")
        return

    cover_path = filedialog.askopenfilename(
        title="Select Playlist Cover Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")]
    )
    if not cover_path:
        messagebox.showinfo("Info", "No cover image selected. Playlist creation cancelled.")
        return

    folder_path = None
    if choice:
        folder_path = filedialog.askdirectory(title="Select Folder with Songs")
        if not folder_path:
            messagebox.showinfo("Info", "No folder selected. Creating an empty playlist.")

    try:
        print(f"Creating playlist '{playlist_name}' with cover '{cover_path}' and folder '{folder_path}'")

        if folder_path:
            create_playlist(user_id=1, folder_path=folder_path, insert_song_function=insert_song)
        else:
            from app.db.database import create_connection
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO playlists (user_id, name, description, playlist_cover_path)
                    VALUES (%s, %s, %s, %s)
                """, (1, playlist_name, "User-created playlist", cover_path))
                connection.commit()
                messagebox.showinfo("Success", f"Empty playlist '{playlist_name}' created successfully!")
                cursor.close()
                connection.close()
        print(f"Playlist '{playlist_name}' created successfully.")

    except Exception as e:
        print(f"Error creating playlist: {e}")
        messagebox.showerror("Error", f"Failed to create playlist: {e}")

def process_playlist_from_files(files):
    connection = create_connection()
    if not connection:
        messagebox.showerror("Error", "Failed to connect to the database.")
        return

    playlist_name = simpledialog.askstring("Playlist Name", "Enter the name of the playlist:")
    if not playlist_name:
        messagebox.showinfo("Info", "Playlist creation cancelled.")
        return

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO playlists (user_id, name, description, created_by, playlist_cover_path)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (1, playlist_name, "Custom playlist", 'User', 'app/gui/assets/covers/song_covers/song_cover.png'))
        connection.commit()
        playlist_id = cursor.lastrowid

        for file_path in files:
            title, ext = os.path.splitext(os.path.basename(file_path))
            insert_song(connection, 1, title, "Unknown Artist", "Unknown Album", "Unknown Genre", file_path, 'app/gui/assets/covers/song_covers/song_cover.png')
            song_id = cursor.lastrowid

            cursor.execute("INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)", (playlist_id, song_id))
            connection.commit()

        messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create playlist: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
