from app.func.utils import fetch_playlists
from tkinter import Label, Button

class Playlist:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class PlaylistManager:
    def __init__(self):
        self.playlists = []

    def load_playlists(self):
        self.playlists = [Playlist(name) for name in fetch_playlists()]
        print(f"Loaded playlists: {[playlist.name for playlist in self.playlists]}")

    def get_playlists(self):
        return self.playlists


def update_playlist_buttons(playlist_frame):
    manager = PlaylistManager()
    manager.load_playlists()

    for widget in playlist_frame.winfo_children():
        widget.destroy()

    if not manager.get_playlists():
        Label(playlist_frame, text="No Playlists Available", fg="#845162", bg="#2d0232").pack(pady=10)
        return

    for playlist in manager.get_playlists():
        Button(
            playlist_frame,
            text=playlist.name,
            font=("Arial", 12),
            fg='#845162',
            bg='#50184A',
            activebackground='#845162',
            activeforeground='#845162',
            command=lambda name=playlist.name: print(f"Selected playlist: {name}")
        ).pack(fill="x", padx=10, pady=5)

class UserSession:
    def __init__(self):
        self.user_id = None
        self.username = None
        # self.email = None

    def set_user(self, user_id, username):
        self.user_id = user_id
        self.username = username
        # self.email = email

    def clear_session(self):
        self.user_id = None
        self.username = None
        # self.email = None


user_session = UserSession()

