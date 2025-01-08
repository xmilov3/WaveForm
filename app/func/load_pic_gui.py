import os
from tkinter import PhotoImage
from PIL import Image, ImageTk

def get_full_path(relative_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)

def load_logo():
    img = PhotoImage(file=get_full_path('../gui/assets/pics/Logo.png'))
    return img

def load_top_logo(size=(100,100)):
    full_path = get_full_path('../gui/assets/pics/TopLogo.png')
    l_top = Image.open(full_path)  
    l_top = l_top.resize(size, Image.LANCZOS)  
    return ImageTk.PhotoImage(l_top)  

def load_text(size=(200, 200)):
    full_path = get_full_path('../gui/assets/pics/waveform.png')  
    img = Image.open(full_path)  
    img = img.resize(size, Image.LANCZOS)  
    return ImageTk.PhotoImage(img)  

def load_default_cover():
    default_cover = PhotoImage(file=get_full_path('../gui/assets/pics/song_cover.png'))
    return default_cover

def load_play_button():
    play_button = PhotoImage(file=get_full_path('../gui/assets/buttons/play_button.png'))
    return play_button

def load_pause_button():
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

def load_default_song_cover():
    default_song_cover = PhotoImage(file=get_full_path('../gui/assets/covers/song_covers/song_cover.png'))
    return default_song_cover