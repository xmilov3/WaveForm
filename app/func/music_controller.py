from tkinter import *
from customtkinter import *
import pygame
import time
from app.func.load_pic_gui import load_play_button, load_pause_button, load_next_button, load_previous_button
from app.func.config import *
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
        print("Folder 'Music' nie znaleziono.")
    except Exception as e:
        print(f"Błąd: {e}")
        
    return song_listbox


# Manipulate song functions
def play_pause_song(currentsong, is_playing, play_button, play_button_img, pause_button_img):
    if not currentsong:
        print("Nie wybrano żadnej piosenki!")
        return is_playing

    if is_playing:
        print("Pauzowanie muzyki")
        play_button.config(image=play_button_img)  
        pygame.mixer.music.pause()
        return False
    else:
        print("Wznawianie muzyki")
        play_button.config(image=pause_button_img) 
        if not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.load(currentsong)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Błąd: {e}")
                return is_playing
        else:
            pygame.mixer.music.unpause()
        return True






    
def stop_song(play_button, play_button_img):
    global is_playing
    pygame.mixer.music.stop()
    play_button.config(image=play_button.image_play)  
    is_playing = False
    return is_playing


    
def next_song(song_listbox, play_button, play_button_img, pause_button_img):
    global currentsong, is_playing
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

    play_button.config(image=pause_button_img)

    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load(currentsong)
        pygame.mixer.music.play()
        is_playing = True  
    except Exception as e:
        print(f"Błąd ładowania piosenki: {e}")
        play_button.config(image=play_button_img) 
        is_playing = False


def previous_song(song_listbox, play_button, play_button_img, pause_button_img):
    global currentsong, is_playing
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

    play_button.config(image=pause_button_img)

    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load(currentsong)
        pygame.mixer.music.play()
        is_playing = True  
    except Exception as e:
        print(f"Błąd ładowania piosenki: {e}")
        play_button.config(image=play_button_img)  
        is_playing = False


    
def now_playing(song_listbox, currentsong, title_label, artist_label, title2_label, artist2_label):
    currentsong = song_listbox.get(ACTIVE)
    currentsong = currentsong.replace('.mp3', '').replace('.wav', '') 
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
        
    return currentsong, title_label, artist_label, title2_label, artist2_label
    
def control_volume(value, volume_label):
    pygame.mixer.music.set_volume(float(value)/100)
    volume_label.configure(text=f"Volume: {int(value)}%")
    
    

def progress_bar(time_remaining_label, time_elapsed_label, progress_slider, bottom_center_bar):
    global current_song_position
    
    if not user_sliding:
        current_time_ms = pygame.mixer.music.get_pos()
        if current_time_ms != -1:  
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
    song_start_time = new_time  
    current_song_position = new_time
    
    time_elapsed_label.configure(text=time.strftime("%M:%S", time.gmtime(new_time)))
    time_remaining_label.configure(text=time.strftime("-%M:%S", time.gmtime(song_length - new_time)))
    bottom_center_bar.after(500, lambda: set_user_sliding(False))

    
def set_user_sliding(value):
    global user_sliding
    user_sliding = value
    return user_sliding


def create_playlist_button(parent, text, bg_color, icon=None):
    return Button(parent, text=text, font=("Arial", 14, "bold"), width=20, height=2, borderwidth=0, highlightthickness=0,
                  activebackground='#501908', cursor='hand2')