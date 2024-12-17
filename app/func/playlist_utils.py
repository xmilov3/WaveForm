import os
from app.db.database import create_connection
from app.func.utils import process_playlist_from_folder, split_title_and_artist
from tkinter import Label, Button, Frame
from app.func.utils import fetch_playlists

def update_playlist_buttons(playlist_frame, delete_playlist_callback):
    for widget in playlist_frame.winfo_children():
        widget.destroy()

    playlists = fetch_playlists()

    if not playlists:
        Label(playlist_frame, text="No Playlists Available", fg="#845162", bg="#2d0232").pack(pady=10)
        return

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
            text="X",
            fg="white",
            bg="red",
            command=lambda name=playlist_name: delete_playlist_callback(name, playlist_frame)
        ).pack(side="right")
