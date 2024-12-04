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
pygame.mixer.init(channels=2)
import mysql.connector



def create_song_listbox(songlist_frame):
    song_listbox = Listbox(
        songlist_frame, 
        bg='#3C0F64', 
        fg='white', 
        selectbackground='#9C27B0', 
        selectforeground='white',
        font=("Arial", 14), 
        relief="flat"
    )
    song_listbox.place(relwidth=1, relheight=1)
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()
        query = "SELECT title, artist FROM songs"
        cursor.execute(query)
        songs = cursor.fetchall()

        for song in songs:
            title, artist = song
            song_listbox.insert(END, f"{title} - {artist}")

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

    return song_listbox

def initialize_first_song(
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
):
    global currentsong, song_length, current_song_position, song_start_time, is_playing

    # Domyślny stan aplikacji
    is_playing = False
    current_song_position = 0
    song_length = 0

    # Ustaw przycisk na "Play" na starcie
    play_pause_button.config(image=play_button_img)

    if song_listbox.size() == 0:
        print("Lista utworów jest pusta!")
        return

    song_listbox.select_set(0)
    song_listbox.activate(0)
    currentsong = song_listbox.get(0)

    try:
        # Pobierz pierwszy utwór z bazy danych
        song_title, artist_name = currentsong.split(" - ")
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()

        query = "SELECT file_path FROM songs WHERE title = %s AND artist = %s"
        cursor.execute(query, (song_title.strip(), artist_name.strip()))
        result = cursor.fetchone()

        if not result:
            print(f"Plik dla utworu {song_title} - {artist_name} nie został znaleziony.")
            return

        file_path = result[0]

        if not os.path.exists(file_path):
            print(f"Plik nie istnieje: {file_path}")
            return

        # Załaduj plik, ale nie odtwarzaj
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.stop()  # Upewnij się, że muzyka jest zatrzymana

        song_length = MP3(file_path).info.length
        time_elapsed_label.config(text="00:00")
        time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(song_length)))
        progress_slider.set(0)

        update_song_info(currentsong, title_label, artist_label)
    except Exception as e:
        print(f"Błąd przy inicjalizacji pierwszego utworu: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()




def play_pause_song(song_info, is_playing, play_button, play_button_img, pause_button_img, title_label, artist_label):

    try:
        song_title, artist_name = song_info.split(" - ")
        
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()

        query = "SELECT file_path FROM songs WHERE title = %s AND artist = %s"
        cursor.execute(query, (song_title.strip(), artist_name.strip()))
        result = cursor.fetchone()

        if not result:
            print(f"File path not found for song: {song_title} by {artist_name}")
            return is_playing

        file_path = result[0]

        if not os.path.exists(file_path):
            print(f"No file found at: {file_path}")
            return is_playing

        if is_playing:
            print(f"Pausing song: {song_title}")
            pygame.mixer.music.pause()  
            play_button.config(image=play_button_img)  
            return False
        else:
            print(f"Playing song: {song_title}")
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            play_button.config(image=pause_button_img) 
            
            title_label.config(text=song_title) 
            artist_label.config(text=artist_name) 
            
            return True

    except Exception as e:
        print(f"Song playback error: {e}")
        return is_playing
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()





def stop_song(play_button, play_button_img):
    global is_playing, current_song_position, song_start_time
    pygame.mixer.music.stop()
    play_button.config(image=play_button_img)
    is_playing = False
    current_song_position = 0  
    song_start_time = 0  
    print("Song paused")
    return is_playing


def next_song(song_listbox, play_button, play_button_img, pause_button_img, title_label, artist_label, time_elapsed_label, time_remaining_label, progress_slider):
    global currentsong, is_playing, song_length

    if song_listbox.size() == 0:
        print("The song list is empty!")
        return

    current_index = song_listbox.curselection()
    if not current_index:
        print("No song selected!")
        return

    next_index = (current_index[0] + 1) % song_listbox.size()
    song_listbox.select_clear(0, END)
    song_listbox.select_set(next_index)
    song_listbox.activate(next_index)

    currentsong = song_listbox.get(next_index)

    is_playing = play_pause_song(currentsong, False, play_button, play_button_img, pause_button_img, title_label, artist_label)
    progress_slider.set(0)




def previous_song(song_listbox, play_button, play_button_img, pause_button_img, title_label, artist_label, time_elapsed_label, time_remaining_label, progress_slider):
    global currentsong, is_playing, song_length

    if song_listbox.size() == 0:
        print("The song list is empty!")
        return

    current_index = song_listbox.curselection()
    if not current_index:
        print("No song selected!")
        return

    previous_index = (current_index[0] - 1) % song_listbox.size()
    song_listbox.select_clear(0, END)
    song_listbox.select_set(previous_index)
    song_listbox.activate(previous_index)

    currentsong = song_listbox.get(previous_index)

    is_playing = play_pause_song(currentsong, False, play_button, play_button_img, pause_button_img, title_label, artist_label)
    progress_slider.set(0)



    
def now_playing(song_listbox, title_label, artist_label, title2_label, artist2_label):
    currentsong = song_listbox.get(ACTIVE)
    currentsong = currentsong.replace('.mp3', '').replace('.wav', '')  

    if " - " in currentsong:
        title, artist = currentsong.split(" - ", 1)  
        title = title[:20] + '...' if len(title) > 20 else title
        artist = artist[:20] + '...' if len(artist) > 20 else artist
    else:
        title = currentsong[:20] + "..." if len(currentsong) > 20 else currentsong
        artist = "Unknown Artist"  

    title_label.config(text=f"{artist}")  
    artist_label.config(text=f"{title}")  

    if title2_label:
        title2_label.config(text=f"{artist}")
    if artist2_label:
        artist2_label.config(text=f"{title}")

        
def update_song_info(currentsong, title_label, artist_label, artist2_label, title2_label):
    currentsong = currentsong.replace('.mp3', '').replace('.wav', '')

    if " - " in currentsong:
        artist, title = currentsong.split(" - ", 1)
    else:
        artist = "Unknown Artist"
        title = currentsong

    title_label.config(text=f"{title}")
    artist_label.config(text=f"{artist}")
    title2_label.config(text=f"{title}")
    artist2_label.config(text=f"{artist}")

    return currentsong, title_label, artist_label, artist2_label, title2_label
    
def control_volume(value, volume_label):
    pygame.mixer.music.set_volume(float(value)/100)
    volume_label.configure(text=f"Volume: {int(value)}%")
    

def progress_bar(time_remaining_label, time_elapsed_label, progress_slider, bottom_frame):
    global current_song_position, song_length, is_playing, user_sliding

    if is_playing and not user_sliding:
        current_time_ms = pygame.mixer.music.get_pos()  
        if current_time_ms != -1:  
            current_song_position = current_time_ms / 1000.0  

        if song_length > 0:
            remaining_time = song_length - current_song_position
            time_elapsed_label.config(text=time.strftime("%M:%S", time.gmtime(current_song_position)))
            time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(remaining_time)))
            progress_slider.set((current_song_position / song_length) * 100)

    bottom_frame.after(500, lambda: progress_bar(time_remaining_label, time_elapsed_label, progress_slider, bottom_frame))


def slide_music(value, time_elapsed_label, time_remaining_label, bottom_frame):
    global user_sliding, current_song_position, is_playing, song_length

    new_time = (float(value) / 100) * song_length 
    current_song_position = new_time

    if is_playing:
        pygame.mixer.music.play(start=new_time) 
        print(f"Music jumped to position: {new_time:.2f} seconds")
    else:
        pygame.mixer.music.set_pos(new_time)  
        print(f"Paused music moved to position: {new_time:.2f} seconds")

    time_elapsed_label.config(text=time.strftime("%M:%S", time.gmtime(new_time)))
    time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(song_length - new_time)))

    bottom_frame.after(500, lambda: set_user_sliding(False))


def set_user_sliding(value):
    global user_sliding, current_song_position, song_start_time
    print(f"set_user_sliding: {user_sliding} -> {value}")
    user_sliding = value

    if not value:
        song_start_time = current_song_position
        print(f"Updated start time: {song_start_time}s")


def create_playlist_button(parent, text, bg_color, icon=None):
    return Button(parent, text=text, font=("Arial", 14, "bold"), width=20, height=2, borderwidth=0, highlightthickness=0,
                  activebackground='#501908', cursor='hand2')
    
