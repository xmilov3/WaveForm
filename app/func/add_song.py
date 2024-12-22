import os
from app.db.db_operations import insert_song
from app.db.database import create_connection
from app.db.song_operations import insert_song
from app.func.playlist_handler import create_playlist, delete_playlist
from tkinter import messagebox, simpledialog, filedialog
from app.func.playlist_utils import fetch_playlists
from tkinter import Toplevel, Label, Listbox, Scrollbar, Button, filedialog, messagebox


def add_song_with_playlist(page_manager):
    playlists = fetch_playlists()
    if not playlists:
        messagebox.showwarning("Warning", "No playlists available. Add a playlist first.")
        return

    dialog = Toplevel()
    dialog.title("Select Playlist")
    dialog.geometry("400x300")
    dialog.configure(bg="#1E052A")

    Label(
        dialog,
        text="Choose a Playlist:",
        font=("Arial", 12, "bold"),
        fg="white",
        bg="#1E052A"
    ).pack(pady=10)

    playlist_listbox = Listbox(
        dialog,
        font=("Arial", 12),
        height=10,
        bg="#2E0532",
        fg="white",
        selectbackground="#50184A",
        selectforeground="white"
    )
    playlist_listbox.pack(fill="both", expand=True, padx=10, pady=5)

    for playlist_name in playlists:
        playlist_listbox.insert("end", playlist_name)

    def select_song():
        selected_index = playlist_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No playlist selected!")
            return

        selected_playlist = playlist_listbox.get(selected_index)
        file_path = filedialog.askopenfilename(
            title="Select a music file",
            filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")]
        )
        if file_path:
            try:
                add_song(file_path, selected_playlist)
                messagebox.showinfo("Success", f"Song added to playlist '{selected_playlist}'!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add song: {e}")
        else:
            messagebox.showinfo("Info", "No file selected.")

    Button(
        dialog,
        text="OK",
        command=select_song,
        font=("Arial", 12),
        bg="#50184A",
        fg="white",
        activebackground="#845162",
        activeforeground="white"
    ).pack(side="left", padx=20, pady=10)

    Button(
        dialog,
        text="Cancel",
        command=dialog.destroy,
        font=("Arial", 12),
        bg="#50184A",
        fg="white",
        activebackground="#845162",
        activeforeground="white"
    ).pack(side="right", padx=20, pady=10)

def add_song(file_path, playlist_name):
    connection = create_connection()
    if not connection:
        print("Failed to connect to database.")
        return

    try:
        title = os.path.basename(file_path).split('.')[0]
        insert_song(
            connection,
            user_id=1,
            title=title,
            artist="Unknown Artist",
            album=playlist_name,
            genre="Unknown Genre",
            file_path=file_path,
            cover_path="app/gui/assets/covers/song_covers/song_cover.png"
        )
        print(f"Song '{title}' added to playlist '{playlist_name}'.")
    except Exception as e:
        print(f"Error adding song: {e}")
    finally:
        connection.close() 
