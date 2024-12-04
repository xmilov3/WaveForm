from tkinter import *
from app.func.config import *
from PIL import Image, ImageTk


def create_left_panel(parent):
    left_frame = Frame(parent, bg='#1E052A', borderwidth=0, highlightbackground='#845162', highlightthickness=0)
    left_frame.grid(row=1, column=0, sticky='nsew', padx=0, pady=0)

    buttons_frame = Frame(left_frame, bg='#2d0232', borderwidth=0, highlightbackground='#845162', highlightthickness=2)
    buttons_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    add_song_button = Button(
        buttons_frame,
        text="Add Song",
        font=("Arial", 12),
        fg='#845162',  
        bg='#50184A',  
        activebackground='#845162',  
        activeforeground='#845162',  
        borderwidth=0,
        highlightbackground='#845162',
        highlightthickness=1,
        padx=10,
        pady=5
    )
    add_song_button.pack(fill="x", padx=10, pady=5)
    create_playlist_button = Button(
        buttons_frame,
        text="Create Playlist",
        font=("Arial", 12),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        highlightbackground='#845162',
        highlightthickness=1,
        padx=10,
        pady=5
    )
    create_playlist_button.pack(fill="x", padx=10, pady=5)

    analyze_song_button = Button(
        buttons_frame,
        text="Analyze Song",
        font=("Arial", 12),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        highlightbackground='#845162',
        highlightthickness=1,
        padx=10,
        pady=5
    )
    analyze_song_button.pack(fill="x", padx=10, pady=5)

    playlist_frame = Frame(left_frame, bg='#2d0232', borderwidth=0, highlightbackground='#845162', highlightthickness=2)
    playlist_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

    playlist_label = Label(
        playlist_frame,
        text="Playlists",
        font=("Arial", 14, "bold"),
        fg='#845162',
        bg='#2d0232',
        borderwidth=0,
        anchor="w"
    )
    playlist_label.pack(fill="x", padx=10, pady=10)

    playlist1 = Button(
        playlist_frame,
        text="Liked Songs",
        font=("Arial", 12),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        highlightbackground='#845162',
        highlightthickness=1,
        padx=10,
        pady=5
    )
    playlist1.pack(fill="x", padx=10, pady=5)

    playlist2 = Button(
        playlist_frame,
        text="UK Dubstep",
        font=("Arial", 12),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        highlightbackground='#845162',
        highlightthickness=1,
        padx=10,
        pady=5
    )
    playlist2.pack(fill="x", padx=10, pady=5)

    left_frame.grid_rowconfigure(0, weight=1)  
    left_frame.grid_rowconfigure(1, weight=2) 
    left_frame.grid_columnconfigure(0, weight=1)

    return left_frame
