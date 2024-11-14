from tkinter import *
import customtkinter
import io
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image, ImageTk
from app.func.load_pic_gui import load_button_image
from func.config import *



def create_button(parent, text, command, bg_color):
    button = Button(parent, text=text, command=command, bg=bg_color, font=("Arial", 14))
    button.pack(side="left", pady=40, padx=5)
    return button

def create_play_pause_button(parent, command):
    play_button = load_button_image("play")
    play_button = load_button_image("pause")
    
    play_pause_label = Label(parent, image=play_button, bg='#1E052A')
    #play_pause_label.pack(side="left", pady=40, padx=15)
    play_pause_label.bind("<Button-1>", command)
    return play_pause_label
    
    
def create_previous_button(parent, command):
    previous_button = load_button_image("previous")
    
    previous_label = Label(parent, image=previous_button, bg='#1E052A')
    #previous_label.pack(side="left", pady=40, padx=5)
    previous_label.bind("<Button-1>", command)
    return previous_label
    
def create_next_button(parent, command):
    next_button = load_button_image("next")
    
    next_label = Label(parent, image=next_button, bg='#1E052A')
    #next_label.pack(side="left", pady=40, padx=5)
    next_label.bind("<Button-1>", command)
    return next_label

def create_title_artist_labels(bottom_left_widget, now_playing):
    title_label = Label(bottom_left_widget, fg="white", bg='#1E052A', font=("Arial", 18, "bold"))
    title_label.pack(side=TOP, padx=0, pady=10)
    title_label.bind("<Button-1>", now_playing)

    artist_label = Label(bottom_left_widget, fg="white", bg='#1E052A', font=("Arial", 14, "bold"))
    artist_label.pack(side=TOP, padx=7, pady=5)
    artist_label.bind("<Button-1>", now_playing)  # You might want to change the command here if needed
    
    return title_label, artist_label  # Return the labels in case you need to modify them later

def create_time_volume_controls(bottom_center_bar, bottom_frame_right, slide_music, control_volume):
    # Time Elapsed
    time_elapsed_label = customtkinter.CTkLabel(bottom_center_bar, text="00:00")
    time_elapsed_label.pack(side="left", pady=5, padx=5)

    # Progress Slider
    progress_slider = customtkinter.CTkSlider(bottom_center_bar, from_=0, to=100, command=slide_music)
    progress_slider.set(0)
    progress_slider.pack(side="left", pady=5, padx=5, expand=True, fill="x")

    # Time Remaining
    time_remaining_label = customtkinter.CTkLabel(bottom_center_bar, text="-00:00")
    time_remaining_label.pack(side="left", pady=5, padx=5)

    # Volume Control
    volume_label = customtkinter.CTkLabel(bottom_frame_right, text="Volume: 100%")
    volume_label.pack(pady=20)

    volume_bar = customtkinter.CTkSlider(bottom_frame_right, from_=0, to=100, command=control_volume)
    volume_bar.set(100)
    volume_bar.pack(pady=10, fill="x")
    
    return time_elapsed_label, progress_slider, time_remaining_label, volume_label, volume_bar

def load_default_album_art():
    global album_art_label
    try:
        default_image = Image.open(default_cover_path)
        default_image = default_image.resize((300, 300))
        default_image = ImageTk.PhotoImage(default_image)
        album_art_label.image = default_image
        album_art_label.config(image=default_image)
    except Exception as e:
        print("Error loading default album art:", e)
        album_art_label.config(image='')
        album_art_label.image = None
        
        
def display_album_art(current_song):
    global album_art_label, currentsong
    
    filepath = os.path.join('Music', currentsong)
    
    # Sprawdź, czy plik jest w formacie MP3
    if filepath.endswith('.mp3'):
        try:
            audio = MP3(filepath, ID3=ID3)
            album_art_found = False 
            for tag in audio.tags.values():
                if isinstance(tag, APIC):  # Jeśli znaleziono obraz w tagu APIC
                    album_art = Image.open(io.BytesIO(tag.data))
                    album_art = album_art.resize((300, 300))  
                    album_art = ImageTk.PhotoImage(album_art)
                    album_art_label.image = album_art  
                    album_art_label.config(image=album_art)
                    album_art_found = True
                    break
            # Jeśli okładka nie została znaleziona w tagach ID3, wyświetl domyślną
            if not album_art_found:
                load_default_album_art()
        except Exception as e:
            print("Couldn't find song cover in MP3:", e)
            load_default_album_art()

    # Jeśli plik jest w formacie WAV lub innym, wyświetl domyślną okładkę
    elif filepath.endswith('.wav'):
        load_default_album_art()
    else:
        print("Unsupported file format:", filepath)
        load_default_album_art()
        