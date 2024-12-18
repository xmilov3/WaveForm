from tkinter import *
import pygame
import os
import sys
from PIL import Image, ImageTk
from app.func.load_pic_gui import load_top_logo, load_default_cover
from app.gui.panels.top_panel import create_top_panel
from app.gui.panels.left_panel import create_left_panel
from app.gui.panels.middle_panel import create_middle_panel
from app.gui.panels.right_panel import create_right_panel, update_next_in_queue, update_now_playing
from app.gui.panels.bottom_panel import create_bottom_panel
from app.func.music_controller import play_pause_song, stop_song, next_song, previous_song, initialize_first_song
from app.func.config import *
from app.gui.assets.pics import *
from app.gui.assets.buttons import *
from app.func.session import center_window



pygame.mixer.init(channels=2)
pygame.mixer.music.stop() 


def create_app_window():
    root = Tk()
    root.title("WaveForm")
    center_window(root, 1500, 1000)
    root.configure(bg='#150016')
    root.iconphoto(False, load_top_logo())
    
    
    
    # Root Window
    main_frame = Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    top_frame = create_top_panel(main_frame)
    left_frame = create_left_panel(main_frame)
    middle_frame, song_listbox = create_middle_panel(main_frame)
    right_frame, queue_text_label, playlist_label, album_art_label, title_label, artist_label = create_right_panel(
        main_frame, playlist_name="Liked Songs")

    

    bottom_frame, time_remaining_label, time_elapsed_label, progress_slider, title_label, artist_label, play_pause_button, play_button_img, pause_button_img = create_bottom_panel(
        main_frame, 
        song_listbox, 
        queue_text_label, 
        "Liked Songs",
        playlist_label, 
        album_art_label, 
        title_label, 
        artist_label, 
        update_next_in_queue, 
        update_now_playing
    )

    initialize_first_song(
        song_listbox, 
        play_pause_button, 
        play_button_img, 
        pause_button_img, 
        title_label, 
        artist_label, 
        time_elapsed_label, 
        time_remaining_label, 
        progress_slider, 
        bottom_frame
    )
    
    # Main Frame
    main_frame.grid_columnconfigure(0, weight=3)
    main_frame.grid_columnconfigure(1, weight=5)
    main_frame.grid_columnconfigure(2, weight=2)
    main_frame.grid_rowconfigure(0, weight=0)
    main_frame.grid_rowconfigure(1, weight=4)
    main_frame.grid_rowconfigure(2, weight=0)
    
    # Top Frame
    top_frame.grid_columnconfigure(0, weight=1)
    
    # Left Frame
    left_frame.grid_rowconfigure(0,  weight=1)
    left_frame.grid_rowconfigure(1,  weight=10)
    left_frame.grid_columnconfigure(0, weight=1)

    
    # Middle Frame
    middle_frame.grid_rowconfigure(0,  weight=1)
    middle_frame.grid_rowconfigure(1,  weight=3)
    middle_frame.grid_columnconfigure(0, weight=1)

    # Right Frame 
    right_frame.grid_rowconfigure(0, weight=5)
    right_frame.grid_rowconfigure(1, weight=4)
    right_frame.grid_columnconfigure(0, weight=1)

    # Bottom frame grid
    bottom_frame.grid_rowconfigure(0, weight=1)
    bottom_frame.grid_rowconfigure(1, weight=0)
    bottom_frame.grid_rowconfigure(2, weight=1)
    bottom_frame.grid_columnconfigure(0, weight=3)
    bottom_frame.grid_columnconfigure(1, weight=6)
    bottom_frame.grid_columnconfigure(2, weight=1)
    
    
    return root


