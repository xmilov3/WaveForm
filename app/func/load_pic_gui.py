import os
from tkinter import PhotoImage

def get_full_path(relative_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)

def load_logo():
    img = PhotoImage(file=get_full_path('../gui/assets/pics/Logo.png'))
    return img

def load_top_logo():
    logo_top = PhotoImage(file=get_full_path('../gui/assets/pics/TopLogo.png'))
    return logo_top

def load_default_cover():
    default_cover = PhotoImage(file=get_full_path('../gui/assets/pics/song_cover.png'))
    return default_cover

def load_play_button():
    print("Ładowanie przycisku Play")  
    play_button = PhotoImage(file=get_full_path('../gui/assets/buttons/play_button.png'))
    return play_button

def load_pause_button():
    print("Ładowanie przycisku Pause")   
    pause_button = PhotoImage(file=get_full_path('../gui/assets/buttons/pause_button.png'))
    return pause_button

def load_next_button():
    next_button = PhotoImage(file=get_full_path('../gui/assets/buttons/next_button.png'))
    return next_button

def load_previous_button():
    previous_button = PhotoImage(file=get_full_path('../gui/assets/buttons/previous_button.png'))
    return previous_button

def load_init_logo():
    init_logo = PhotoImage(file=get_full_path('../gui/assets/pics/text_logo.png'))
    return init_logo