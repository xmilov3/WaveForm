from tkinter import *
from customtkinter import *
import pygame
import time
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image, ImageTk
import os
import customtkinter
from app.func.load_pic_gui import load_play_button, load_pause_button, load_next_button, load_previous_button
from app.func.config import *
from app.func.config import artist_label, title_label
pygame.mixer.init(channels=2)



def create_song_listbox(songlist_frame):
    song_listbox = Listbox(songlist_frame, bg='#3C0F64', fg='white', relief="flat")
    song_listbox.place(relwidth=1, relheight=1)

    try:
        os.chdir('Music')
        songs = os.listdir()
        for song in songs:
            if song.endswith('.mp3') or song.endswith('.wav'): 
                song_listbox.insert(END, song)
    except FileNotFoundError:
        print("Folder 'Music' not found.")
    except Exception as e:
        print(f"Error: {e}")
        
    return song_listbox

def initialize_first_song(song_listbox, time_remaining_label, time_elapsed_label, progress_slider, bottom_frame, title_label, artist_label):
    global currentsong, song_length, current_song_position, song_start_time, is_playing

    is_playing = False
    song_listbox.select_set(0)
    song_listbox.activate(0)
    currentsong = song_listbox.get(0)

    try:
        pygame.mixer.music.load(currentsong)
        song_length = pygame.mixer.Sound(currentsong).get_length()
        current_song_position = 0
        song_start_time = 0

        now_playing(currentsong, title_label, artist_label)  

        time_elapsed_label.config(text="00:00")
        time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(song_length)))
        progress_slider.set(0)

        pygame.mixer.music.play()  
    except Exception as e:
        print(f"Error initializing first track: {e}")











# Manipulate song functions
def play_pause_song(currentsong, is_playing, play_button, play_button_img, pause_button_img, title_label, artist_label):
    global current_song_position, song_start_time, song_length

    if not currentsong:
        print("No song selected!")
        return is_playing

    if is_playing:
        pygame.mixer.music.pause()
        current_song_position = pygame.mixer.music.get_pos() / 1000
        play_button.config(image=play_button_img)
        is_playing = False
        print(f"Song paused at position: {current_song_position}s")
    else:
        if current_song_position > 0:
            pygame.mixer.music.unpause()
        else:
            try:
                pygame.mixer.music.load(currentsong)
                pygame.mixer.music.play()
                song_length = pygame.mixer.Sound(currentsong).get_length()
                current_song_position = 0
                song_start_time = 0
                print(f"Start playing: {currentsong}, lenght: {song_length}s")
            except Exception as e:
                print(f"Song playback error: {e}")
                return is_playing

        play_button.config(image=pause_button_img)
        is_playing = True

        update_song_info(currentsong, title_label, artist_label)

    return is_playing









    
def stop_song(play_button, play_button_img):
    global is_playing, current_song_position, song_start_time
    pygame.mixer.music.stop()
    play_button.config(image=play_button_img)
    is_playing = False
    current_song_position = 0  
    song_start_time = 0  
    print("Song paused")
    return is_playing


def next_song(song_listbox, play_button, play_button_img, pause_button_img, title_label, artist_label):
    global currentsong, is_playing, current_song_position, song_start_time, song_length

    if song_listbox.size() == 0:
        print("Lista piosenek jest pusta!")
        return

    current_index = song_listbox.curselection()
    if not current_index:
        print("Brak wybranej piosenki!")
        return

    next_index = (current_index[0] + 1) % song_listbox.size()
    song_listbox.select_clear(0, END)
    song_listbox.select_set(next_index)
    song_listbox.activate(next_index)

    currentsong = song_listbox.get(next_index)

    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load(currentsong)
        pygame.mixer.music.play()
        song_length = pygame.mixer.Sound(currentsong).get_length()
        current_song_position = 0
        song_start_time = 0
        is_playing = True

        # Aktualizuj informacje o utworze
        now_playing(song_listbox, title_label, artist_label)

    except Exception as e:
        print(f"Błąd ładowania piosenki: {e}")
        play_button.config(image=play_button_img)
        is_playing = False












def previous_song(song_listbox, play_button, play_button_img, pause_button_img, title_label, artist_label):
    global currentsong, is_playing, current_song_position, song_start_time, song_length

    if song_listbox.size() == 0:
        print("Lista piosenek jest pusta!")
        return

    current_index = song_listbox.curselection()
    if not current_index:
        print("Brak wybranej piosenki!")
        return

    previous_index = (current_index[0] - 1) % song_listbox.size()
    song_listbox.select_clear(0, END)
    song_listbox.select_set(previous_index)
    song_listbox.activate(previous_index)

    currentsong = song_listbox.get(previous_index)

    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load(currentsong)
        pygame.mixer.music.play()
        song_length = pygame.mixer.Sound(currentsong).get_length()
        current_song_position = 0
        song_start_time = 0
        is_playing = True

        # Aktualizuj informacje o utworze
        now_playing(song_listbox, title_label, artist_label)

    except Exception as e:
        print(f"Błąd ładowania piosenki: {e}")
        play_button.config(image=play_button_img)
        is_playing = False







    
def now_playing(song_listbox, title_label, artist_label, title2_label=None, artist2_label=None):
    currentsong = song_listbox.get(ACTIVE)
    currentsong = currentsong.replace('.mp3', '').replace('.wav', '')  # Usuń rozszerzenie pliku

    if " - " in currentsong:
        artist, title = currentsong.split(" - ", 1)  # Tylko pierwsze wystąpienie separatora
        title = title[:20] + '...' if len(title) > 20 else title
        artist = artist[:20] + '...' if len(artist) > 20 else artist
    else:
        title = currentsong[:20] + "..." if len(currentsong) > 20 else currentsong
        artist = "Unknown Artist"  # Domyślny artysta, jeśli brak separatora

    title_label.config(text=f"{title}")
    artist_label.config(text=f"{artist}")

    if title2_label:
        title2_label.config(text=f"{title}")
    if artist2_label:
        artist2_label.config(text=f"{artist}")
        
def update_song_info(currentsong, title_label, artist_label):
    currentsong = currentsong.replace('.mp3', '').replace('.wav', '')

    if " - " in currentsong:
        artist, title = currentsong.split(" - ", 1)
    else:
        artist = "Unknown Artist"
        title = currentsong

    title_label.config(text=f"{title}")
    artist_label.config(text=f"{artist}")




        
    return currentsong, title_label, artist_label
    
def control_volume(value, volume_label):
    pygame.mixer.music.set_volume(float(value)/100)
    volume_label.configure(text=f"Volume: {int(value)}%")
    
    

def progress_bar(time_remaining_label, time_elapsed_label, progress_slider, bottom_frame):
    global current_song_position, song_length, is_playing

    if is_playing:
        current_time_ms = pygame.mixer.music.get_pos()
        if current_time_ms != -1:
            current_song_position = current_time_ms / 1000

        if song_length > 0:
            remaining_time = song_length - current_song_position
            time_elapsed_label.config(text=time.strftime("%M:%S", time.gmtime(current_song_position)))
            time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(remaining_time)))
            progress_slider.set((current_song_position / song_length) * 100)

    bottom_frame.after(500, lambda: progress_bar(time_remaining_label, time_elapsed_label, progress_slider, bottom_frame))


def slide_music(value, time_elapsed_label, time_remaining_label, bottom_frame):
    global current_song_position, song_start_time, is_playing, song_length

    new_time = (float(value) / 100) * song_length
    current_song_position = new_time
    song_start_time = new_time

    pygame.mixer.music.stop()
    pygame.mixer.music.play(start=new_time)

    time_elapsed_label.config(text=time.strftime("%M:%S", time.gmtime(new_time)))
    time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(song_length - new_time)))





    
def set_user_sliding(value):
    global user_sliding, current_song_position, song_start_time
    user_sliding = value

    if not value:
        song_start_time = current_song_position
        print(f"Updated start time: {song_start_time}s")




def create_playlist_button(parent, text, bg_color, icon=None):
    return Button(parent, text=text, font=("Arial", 14, "bold"), width=20, height=2, borderwidth=0, highlightthickness=0,
                  activebackground='#501908', cursor='hand2')
    
