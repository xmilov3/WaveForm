from tkinter import Frame, Label
from app.func.config import *


def create_right_panel(main_frame):
    right_frame = Frame(main_frame, bg='#3A0C60')
    right_frame.grid(row=1, column=2, sticky='nsew', padx=1, pady=1)
    
    now_playing_frame = Frame(right_frame, bg='#3A0C60')
    now_playing_frame.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
    now_playing_frame.place(relx=0.07, rely=0.26, anchor="w")
    
    playlist_right_frame_label = Label(now_playing_frame, text='UK Bassline', font=("Arial", 28, "bold"), anchor="w", fg='white', bg='#3A0C60')
    playlist_right_frame_label.pack(fill="x", pady=25)
    
    album_art_label = Label(now_playing_frame)
    album_art_label.pack(fill="both", expand=True, pady=2)
    
    title2_label = Label(now_playing_frame, fg="white",  bg='#3A0C60', font=("Arial", 20, "bold"), anchor="w")
    title2_label.pack(fill="x", pady=5)
    
    artist2_label = Label(now_playing_frame, fg="gray",  bg='#3A0C60', font=("Arial", 16), anchor="w")
    artist2_label.pack(fill="x")
    
    next_in_queue_frame = Frame(right_frame, bg='#3C0F64')
    next_in_queue_frame.grid(row=1, column=0, sticky='nsew', padx=0, pady=1)
    
    return right_frame