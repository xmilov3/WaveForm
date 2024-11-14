from tkinter import *
from app.func.config import *


def create_left_panel(parent):
    left_frame = Frame(parent, bg='#3A0C60')
    left_frame.grid(row=1, column=0, sticky='nsew', padx=1, pady=1)
    search_frame = Frame(left_frame, bg='#3A0C60')
    search_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
    search_type_frame = Frame(search_frame, bg='#3A0C60')
    search_type_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
    Label(search_type_frame, text="Search", font=("Arial", 14), fg='white', bg='#3A0C60')
    search_entry = Entry(search_type_frame, font=("Arial", 12), width=30)
    search_entry.pack(side=LEFT, padx=5, pady=5, fill="x", expand=True)
    search_buttons_frame = Frame(search_frame, bg='blue')
    search_buttons_frame.grid(row=1, column=0, sticky='nsew', padx=1, pady=1)
    Label(search_buttons_frame, text="Buttons_to_search", font=("Arial", 14), fg='white', bg='#3A0C60').pack(pady=5)
    pinned_playlist_frame = Frame(left_frame, bg='red')
    pinned_playlist_frame.grid(row=1, column=0, sticky='nsew', padx=1, pady=1)
    Label(pinned_playlist_frame, text="Playlists", font=("Arial", 14), fg='white', bg='#3A0C60').pack(pady=5)
    playlist1 = Button(pinned_playlist_frame, text="Liked songs", width=20, height=2, fg='black', bg='red')
    playlist1.pack(pady=5)
    playlist2 = Button(pinned_playlist_frame, text="UK Dubstep", width=20, height=2, fg='black', bg='black')
    playlist2.pack(pady=5)
    return left_frame