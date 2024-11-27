from tkinter import *
from app.func.config import *
from app.func.music_controller import create_song_listbox


def create_middle_panel(parent):
    middle_frame = Frame(parent, bg='#3C0F64')
    middle_frame.grid(row=1, column=1, sticky='nsew', padx=1, pady=1)

    header_frame = Frame(middle_frame, bg='#3A0C60')
    header_frame.grid(row=0, columnspan=3, sticky='nsew', padx=1, pady=1)
    Label(header_frame, text='Playlist: UK Bassline', font=("Arial", 24, "bold"), fg='white', bg='#3A0C60').pack(pady=1)
    
    songlist_frame = Frame(middle_frame, bg='black')
    songlist_frame.grid(row=1, columnspan=3, sticky='nsew', padx=1, pady=1)
    song_listbox = create_song_listbox(songlist_frame)
    return middle_frame, song_listbox
    
    
    