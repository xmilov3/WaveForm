from tkinter import *
from customtkinter import *
import pygame
import time
# from app.gui.widgets import create_play_pause_button
from app.func.load_pic_gui import load_button_image
from app.func.config import *
pygame.mixer.init(channels=2)


def create_song_listbox(songlist_frame):
    song_listbox = Listbox(songlist_frame, bg='#3C0F64', fg='white', relief="flat")
    song_listbox.place(relwidth=1, relheight=1)

    os.chdir('Music')
    
    songs = os.listdir()
    
    for s in songs:
        song_listbox.insert(END, s)

    return song_listbox  

# Manipulate song functions
def play_pause_song(currentsong, is_playing, song_listbox, play_pause_label, song_length, current_song_position, song_start_time):
    if is_playing:
        pygame.mixer.music.pause()
        play_pause_label.config(play_pause_label)
    else:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(currentsong)
            current_song_position = 0
            song_start_time = 0
            pygame.mixer.music.play()
            song_length = int(pygame.mixer.Sound(currentsong).get_length())
            now_playing()
            #display_album_art(currentsong)
            progress_bar()
        else:
            pygame.mixer.music.unpause()
        now_playing()
        play_pause_label.config(play_pause_label)
    is_playing = not is_playing
    return is_playing, song_length, current_song_position, song_start_time, song_listbox
    
def stop_song():
    global is_playing
    pygame.mixer.music.stop()
    #play_pause_label.config(image=play_button)
    is_playing = False
    
def next_song(song_listbox):
    global is_playing
    stop_song()
    current_index = song_listbox.curselection()[0]
    next_index = (current_index + 1) % song_listbox.size()
    song_listbox.select_clear(0, END)
    song_listbox.select_set(next_index)
    song_listbox.activate(next_index)
    play_pause_song()
    
def previous_song(song_listbox):
    global is_playing
    stop_song()
    current_index = song_listbox.curselection()[0]
    previous_index = (current_index - 1) % song_listbox.size()
    song_listbox.select_clear(0, END)
    song_listbox.select_set(previous_index)
    song_listbox.activate(previous_index)
    play_pause_song()
    
def now_playing(song_listbox, title_label, artist_label, title2_label, artist2_label):
    global is_playing, currentsong
    currentsong = song_listbox.get(ACTIVE)
    currentsong = currentsong.replace('.mp3', '').replace('.wav', '') # Hide extension
    # Cut too long title
    if " - " in currentsong:
        artist, title = currentsong.split(" - ")
        title = title[:20] + '...' if len(title) > 20 else title
        artist = artist[:20] + '...' if len(artist) > 20 else artist
        title_label.config(text=f"{title}")
        artist_label.config(text=f"{artist}")
        title2_label.config(text=f"{title}")
        artist2_label.config(text=f"{artist}")
        
    else:
        currentsong_display = currentsong[:20] + "..." if len(currentsong) > 20 else currentsong
        title_label.config(text=f"{currentsong_display}")
        artist_label.config(text=f"{currentsong_display}")
        title2_label.config(text=f"{currentsong_display}")
        artist2_label.config(text=f"{currentsong_display}")
        
    
def control_volume(value, volume_label):
    pygame.mixer.music.set_volume(float(value)/100)
    volume_label.configure(text=f"Volume: {int(value)}%")
    

def progress_bar(time_remaining_label, time_elapsed_label, progress_slider, bottom_center_bar):
    global current_song_position
    
    if not user_sliding:
        current_time_ms = pygame.mixer.music.get_pos()
        if current_time_ms != -1:  # Check if music is playing
            current_song_position = int(current_time_ms / 1000) + song_start_time
        
        remaining_time = song_length - current_song_position
        time_elapsed_label.configure(text=time.strftime("%M:%S", time.gmtime(current_song_position)))
        time_remaining_label.configure(text=time.strftime("-%M:%S", time.gmtime(remaining_time)))

        if song_length > 0:
            progress_slider.set((current_song_position / song_length) * 100)
                
    if pygame.mixer.music.get_busy():
        bottom_center_bar.after(1000, progress_bar)

def slide_music(value, time_elapsed_label, time_remaining_label, bottom_center_bar):
    global user_sliding, current_song_position, song_start_time
    user_sliding = True
    new_time = (float(value) / 100) * song_length
    
    pygame.mixer.music.stop()
    pygame.mixer.music.play(start=new_time)
    song_start_time = new_time  # Store the start time for get_pos() calculations
    current_song_position = new_time
    
    time_elapsed_label.configure(text=time.strftime("%M:%S", time.gmtime(new_time)))
    time_remaining_label.configure(text=time.strftime("-%M:%S", time.gmtime(song_length - new_time)))
    bottom_center_bar.after(500, lambda: set_user_sliding(False))

    
def set_user_sliding(value):
    global user_sliding
    user_sliding = value

# def create_widgets(self):
#     self.create_bottom_widgets()
    
# def create_bottom_widgets(self):
#     self.create_
    
# Left panel buttons
def create_playlist_button(parent, text, bg_color, icon=None):
    return Button(parent, text=text, font=("Arial", 14, "bold"), width=20, height=2, borderwidth=0, highlightthickness=0,
                  activebackground='#501908', cursor='hand2')