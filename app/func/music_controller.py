from tkinter import *
from customtkinter import *
import pygame
import time
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image, ImageTk
import os
import customtkinter
from app.func.config import *
pygame.mixer.init(channels=2)
import mysql.connector
from pydub import AudioSegment
from app.gui.panels.right_panel import update_next_in_queue, update_now_playing



def create_song_listbox(songlist_frame):
    song_listbox = Listbox(
        songlist_frame, 
        bg='#3C0F64', 
        fg='grey', 
        selectbackground='#9C27B0', 
        selectforeground='grey',
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

def sync_is_playing():
    global is_playing
    is_playing = pygame.mixer.music.get_busy()
    print(f"Synced is_playing: {is_playing}")



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

    if song_listbox.size() == 0:
        print("The song list is empty!")
        return

    is_playing = False
    current_song_position = 0
    song_start_time = 0
    song_length = 0
    pygame.mixer.music.stop()

    song_listbox.select_clear(0, END)
    song_listbox.select_set(0)
    song_listbox.activate(0)

    currentsong = song_listbox.get(0)
    if not currentsong:
        print("Error: No song selected or song_info is None.")
        return

    try:
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
            print(f"File for song {song_title} - {artist_name} not found.")
            return

        file_path = result[0]

        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            return

        file_extension = os.path.splitext(file_path)[-1].lower()

        if file_extension == ".mp3":
            pygame.mixer.music.load(file_path)
            song_length = MP3(file_path).info.length
        elif file_extension == ".wav":
            audio = AudioSegment.from_file(file_path, format="wav")
            pygame.mixer.music.load(file_path)
            song_length = len(audio) / 1000.0 
        else:
            print(f"Unsupported file format: {file_extension}")
            return

        play_pause_button.config(image=play_button_img) 
        time_elapsed_label.config(text="00:00")
        time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(song_length)))
        progress_slider.set(0)
        title_label.config(text=song_title)
        artist_label.config(text=artist_name)

        print(f"First song initialized: {song_title} - {artist_name}")

    except Exception as e:
        print(f"Error in initialize_first_song: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

    sync_is_playing()





def play_pause_song(song_info, is_playing, play_button, play_button_img, pause_button_img, title_label, artist_label):
    global current_song_position, song_start_time

    try:
        if not song_info:
            print("Error, Song info not found!")
            return is_playing

        song_title, artist_name = song_info.split(" - ")

        if pygame.mixer.music.get_busy():
            is_playing = True
        else:
            is_playing = False

        if is_playing:
            print(f"Pausing song: {song_title}")
            current_song_position = pygame.mixer.music.get_pos() / 1000.0
            pygame.mixer.music.pause()
            play_button.config(image=play_button_img)
            is_playing = False
        else:
            if current_song_position > 0:
                print(f"Resuming song: {song_title} from position {current_song_position:.2f}s")
                pygame.mixer.music.unpause()
            else:
                print(f"Starting song: {song_title} from the beginning")
                pygame.mixer.music.play()
                current_song_position = 0
                song_start_time = 0
            play_button.config(image=pause_button_img)
            is_playing = True
            sync_is_playing()

        return is_playing

    except Exception as e:
        print(f"Błąd w play_pause_song: {e}")
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
    sync_is_playing()


def next_song(song_listbox, play_pause_button, play_button_img, pause_button_img, 
              title_label, artist_label, time_elapsed_label, time_remaining_label, 
              progress_slider, queue_text_label, playlist_name, playlist_label, album_art_label):
    global currentsong, is_playing, current_song_position, song_length, song_start_time

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
    song_title, artist_name = currentsong.split(" - ")

    update_next_in_queue(queue_text_label, playlist_name)
    update_now_playing(playlist_label, album_art_label, title_label, artist_label, playlist_name)

    try:
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
            print(f"File for song {song_title} - {artist_name} not found.")
            return

        file_path = result[0]

        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            return

        file_extension = os.path.splitext(file_path)[-1].lower()

        if file_extension == ".mp3":
            try:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                song_length = MP3(file_path).info.length
            except Exception as e:
                print(f"Error loading MP3 file: {e}")
                return

        elif file_extension == ".wav":
            try:
                audio = AudioSegment.from_file(file_path, format="wav")
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                song_length = len(audio) / 1000.0
            except Exception as e:
                print(f"Error loading WAV file: {e}")
                return

        else:
            print(f"Unsupported file format: {file_extension}")
            return

        current_song_position = 0
        song_start_time = 0
        is_playing = True

        play_pause_button.config(image=pause_button_img)
        time_elapsed_label.config(text="00:00")
        time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(song_length)))
        progress_slider.set(0)
        title_label.config(text=song_title)
        artist_label.config(text=artist_name)

    except Exception as e:
        print(f"Error in next_song: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
    sync_is_playing()



def previous_song(song_listbox, play_pause_button, play_button_img, pause_button_img, 
                  title_label, artist_label, time_elapsed_label, time_remaining_label, 
                  progress_slider, queue_text_label, playlist_name, playlist_label, album_art_label):   
    global currentsong, is_playing, current_song_position, song_length, song_start_time

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
    song_title, artist_name = currentsong.split(" - ")

    update_next_in_queue(queue_text_label, playlist_name)
    update_now_playing(playlist_label, album_art_label, title_label, artist_label, playlist_name)

    try:
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
            print(f"File for song {song_title} - {artist_name} not found.")
            return

        file_path = result[0]

        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            return

        file_extension = os.path.splitext(file_path)[-1].lower()

        if file_extension == ".mp3":
            try:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                song_length = MP3(file_path).info.length
            except Exception as e:
                print(f"Error playing MP3: {e}")
                return

        elif file_extension == ".wav":
            try:
                audio = AudioSegment.from_file(file_path, format="wav")
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                song_length = len(audio) / 1000.0
            except Exception as e:
                print(f"Error playing WAV: {e}")
                return

        else:
            print(f"Unsupported file format: {file_extension}")
            return

        current_song_position = 0
        song_start_time = 0
        is_playing = True

        play_pause_button.config(image=pause_button_img)
        time_elapsed_label.config(text="00:00")
        time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(song_length)))
        progress_slider.set(0)
        title_label.config(text=song_title)
        artist_label.config(text=artist_name)

    except Exception as e:
        print(f"Error in previous_song: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
    sync_is_playing()






    
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
            current_song_position = current_time_ms / 1000.0 + song_start_time

        if song_length > 0:
            remaining_time = song_length - current_song_position
            time_elapsed_label.config(text=time.strftime("%M:%S", time.gmtime(current_song_position)))
            time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(remaining_time)))
            progress_slider.set((current_song_position / song_length) * 100)

    bottom_frame.after(500, lambda: progress_bar(time_remaining_label, time_elapsed_label, progress_slider, bottom_frame))

def slide_music(value, time_elapsed_label, time_remaining_label, bottom_frame, progress_slider, play_pause_button, play_button_img, pause_button_img, currentsong):
    global user_sliding, current_song_position, is_playing, song_length

    user_sliding = True

    new_time = (float(value) / 100) * song_length
    current_song_position = new_time

    if is_playing:
        pygame.mixer.music.stop()
        # pygame.mixer.music.set_pos(new_time)
        pygame.mixer.music.play(start=new_time)
        print(f"Music jumped to position: {new_time:.2f} seconds")
    else:
        pygame.mixer.music.stop()
        # pygame.mixer.music.load(currentsong)
        pygame.mixer.music.play(start=new_time)
        pygame.mixer.music.pause()
        print("Music position updated and paused")

    time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(song_length - new_time)))
    progress_slider.set((new_time / song_length) * 100)

    bottom_frame.after(100, lambda: set_user_sliding(False))




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