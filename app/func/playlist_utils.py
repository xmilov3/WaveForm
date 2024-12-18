import os
from app.db.database import create_connection
from app.func.utils import process_playlist_from_folder, split_title_and_artist
from tkinter import Label, Button, Frame, messagebox, filedialog
from app.func.utils import fetch_playlists

from tkinter import Menu

def update_playlist_buttons(playlist_frame, delete_playlist_callback, change_cover_callback):
    from app.func.utils import fetch_playlists

    for widget in playlist_frame.winfo_children():
        widget.destroy()

    playlists = fetch_playlists()

    for playlist_name in playlists:
        frame = Frame(playlist_frame, bg="#2d0232")
        frame.pack(fill="x", padx=10, pady=5)

        Button(
            frame,
            text=playlist_name,
            command=lambda name=playlist_name: print(f"Selected playlist: {name}")
        ).pack(side="left", fill="x", expand=True)

        Button(
            frame,
            text=":",
            fg="white",
            bg="#50184A",
            command=lambda name=playlist_name: show_playlist_menu(name, delete_playlist_callback, change_cover_callback)
        ).pack(side="right")




def show_playlist_menu(playlist_name, delete_playlist_callback, change_cover_callback):
    menu = Menu(None, tearoff=0)
    menu.add_command(label="Delete Playlist", command=lambda: delete_playlist_callback(playlist_name))
    menu.add_command(
    label="Delete Playlist",
    command=lambda: delete_playlist_callback(playlist_name, update_playlist_buttons)
)

    menu.add_command(label="Change Cover", command=lambda: change_cover_callback(playlist_name))
    menu.post(500, 500)


def open_playlist_menu(parent, playlist_name, delete_callback, change_cover_callback):
    menu = Menu(parent, tearoff=0)
    menu.add_command(label="Delete Playlist", command=lambda: delete_callback(playlist_name, parent))
    menu.add_command(label="Change Cover", command=lambda: change_cover_callback(playlist_name))
    menu.post(parent.winfo_rootx(), parent.winfo_rooty())

def change_playlist_cover(playlist_name):
    cover_path = filedialog.askopenfilename(
        title="Select New Playlist Cover",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")]
    )
    if not cover_path:
        messagebox.showinfo("Info", "No cover image selected.")
        return

    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = "UPDATE playlists SET playlist_cover_path = %s WHERE name = %s"
        cursor.execute(query, (cover_path, playlist_name))
        connection.commit()

        messagebox.showinfo("Success", f"Cover updated for playlist '{playlist_name}'!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update cover: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
