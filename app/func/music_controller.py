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
from app.func.shared_func import play_playlist



currentsong = None
song_length = 0
current_song_position = 0
song_start_time = 0
is_playing = False
user_sliding = False




def initialize_song_listbox(parent, playlist_name, album_art_label, play_song_callback, title_label, artist_label, time_elapsed_label, time_remaining_label, progress_slider):
    song_listbox = Listbox(
        parent,
        bg='#2D0232',
        fg='grey',
        selectforeground='grey',
        font=("Arial", 14),
        relief="flat"
    )
    song_listbox.grid(sticky="nsew", padx=5, pady=5)

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    populate_song_listbox(song_listbox, playlist_name)

    song_listbox.bind("<Double-1>", lambda event: play_song_callback(
        song_listbox.get(ACTIVE),
        title_label,
        artist_label,
        album_art_label,
        time_elapsed_label,
        time_remaining_label,
        progress_slider
    ))

    return song_listbox


def populate_song_listbox(song_listbox, playlist_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()

        query = """
            SELECT 
                s.title AS song_title,
                s.artist AS song_artist
            FROM songs s
            JOIN playlist_songs ps ON s.song_id = ps.song_id
            JOIN playlists p ON ps.playlist_id = p.playlist_id
            WHERE p.name = %s
        """
        cursor.execute(query, (playlist_name,))
        songs = cursor.fetchall()

        song_listbox.delete(0, END)

        for title, artist in songs:
            song_listbox.insert(END, f"{title} - {artist}")

        if not songs:
            song_listbox.insert(END, "Playlist is empty.")
            print(f"Playlist is empty: {playlist_name}")

    except mysql.connector.Error as e:
        print(f"Error while loading song_listbox: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()





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
    bottom_frame,
    playlist_name=None
):
    global currentsong, song_length, current_song_position, song_start_time, is_playing, play_playlist
        

    if playlist_name:
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='WaveForm_db',
                user='root',
                password=''
            )
            cursor = connection.cursor()
            query = """
                SELECT s.title, s.artist
                FROM songs s
                JOIN playlist_songs ps ON s.song_id = ps.song_id
                JOIN playlists p ON ps.playlist_id = p.playlist_id
                WHERE p.name = %s
                ORDER BY ps.song_id ASC
            """
            cursor.execute(query, (playlist_name,))
            songs = cursor.fetchall()

            song_listbox.delete(0, END)
            for song in songs:
                song_listbox.insert(END, f"{song[0]} - {song[1]}")
                song_listbox.select_set(0)
                song_listbox.activate(0)

            if not songs:
                print(f"No songs found for playlist: {playlist_name}")
                return

        except Exception as e:
            print(f"Error loading songs for playlist: {e}")
            return
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

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
    song_listbox.see(0)

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

def handle_double_click(song_listbox, play_pause_button, play_button_img, pause_button_img, title_label, artist_label, time_elapsed_label, time_remaining_label, progress_slider, album_art_label):
    global currentsong
    
    



    selected_index = song_listbox.curselection()
    if not selected_index:
        return

    song_listbox.selection_clear(0, END)
    song_listbox.selection_set(selected_index)
    song_listbox.activate(selected_index)
    song_listbox.see(selected_index)

    currentsong = song_listbox.get(selected_index)
    
    play_selected_song(
        currentsong,
        title_label,
        artist_label,
        album_art_label,
        time_elapsed_label,
        time_remaining_label,
        progress_slider,
        play_pause_button,
        pause_button_img
    )

    if hasattr(play_pause_button, 'current_playlist'):
        if hasattr(play_pause_button, 'queue_text_label'):
            update_next_in_queue(play_pause_button.queue_text_label, play_pause_button.current_playlist)
        if hasattr(play_pause_button, 'playlist_label'):
            update_now_playing(play_pause_button.playlist_label, album_art_label, title_label, artist_label, play_pause_button.current_playlist)
        play_pause_button.config(image=pause_button_img)
    

def select_song_from_list(song_listbox, play_pause_button, play_button_img, pause_button_img, title_label, artist_label, time_elapsed_label, time_remaining_label, progress_slider, album_art_label):
    global currentsong, song_length, current_song_position, song_start_time, is_playing
    selected_index = song_listbox.curselection()
    if not selected_index:
        print("No song selected!")
        return
    
    pygame.mixer.music.stop()
    current_song_position = 0
    song_start_time = 0
    is_playing = False
    
    currentsong = song_listbox.get(selected_index)
    if not currentsong:
        print("Error: no song selected!")
        return
        
    play_selected_song(
        currentsong,
        title_label,
        artist_label,
        album_art_label,
        time_elapsed_label,
        time_remaining_label,
        progress_slider,
        play_pause_button,
        pause_button_img
    )

def play_selected_song(selected_song, title_label, artist_label, album_art_label, time_elapsed_label, time_remaining_label, progress_slider, play_pause_button=None, pause_button_img=None):
    global is_playing, song_length, current_song_position, song_start_time
    
    is_playing = True
    current_song_position = 0
    song_start_time = 0

    try:
        if " - " not in selected_song:
            print("Wrong song format!")
            return

        song_title, artist_name = selected_song.split(" - ")
        
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()

        query = "SELECT file_path, cover_path FROM songs WHERE title = %s AND artist = %s"
        cursor.execute(query, (song_title.strip(), artist_name.strip()))
        result = cursor.fetchone()

        if not result:
            print(f"No file found for {song_title} - {artist_name}")
            return

        file_path, cover_path = result

        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            return

        file_extension = os.path.splitext(file_path)[-1].lower()
        
        if file_extension == ".mp3":
            song_length = MP3(file_path).info.length
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        elif file_extension == ".wav":
            audio = AudioSegment.from_file(file_path, format="wav")
            song_length = len(audio) / 1000.0
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        else:
            print(f"Unsupported file format: {file_path}")
            return

        time_elapsed_label.config(text="00:00")
        time_remaining_label.config(text=f"-{int(song_length // 60):02}:{int(song_length % 60):02}")
        progress_slider.set(0)
        progress_slider.config(to=100)
        title_label.config(text=song_title.strip())
        artist_label.config(text=artist_name.strip())
        
        if play_pause_button and pause_button_img:
            play_pause_button.config(image=pause_button_img)

        if cover_path and os.path.exists(cover_path):
            img = Image.open(cover_path)
            img = img.resize((300, 300), Image.LANCZOS)
            album_image = ImageTk.PhotoImage(img)
            album_art_label.config(image=album_image)
            album_art_label.image = album_image
        else:
            album_art_label.config(image='', text="No cover")

    except Exception as e:
        print(f"Error in play_selected_song: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

    sync_is_playing()





def play_pause_song(song_info, is_playing, play_button, play_button_img, pause_button_img, title_label, artist_label,):
    global current_song_position, song_start_time

    try:
        if not song_info:
            print("Error, Song info not found!")
            return is_playing

        if " - " in song_info:
            song_title, artist_name = song_info.split(" - ")
        else:
            song_title = song_info.strip()
            artist_name = "Unknown Artist"

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
            progress_slider, queue_text_label, playlist_name, playlist_label, album_art_label, bottom_frame_left):
   global currentsong, is_playing, current_song_position, song_length, song_start_time

   if song_listbox.size() == 0:
       print("The song list is empty!")
       return

   if not song_listbox.curselection():
       song_listbox.select_set(0)
       song_listbox.activate(0)
       current_index = (0,)
   else:
       current_index = song_listbox.curselection()

   next_index = (current_index[0] + 1) % song_listbox.size()
   song_listbox.select_clear(0, END)
   song_listbox.select_set(next_index)
   song_listbox.activate(next_index)

   currentsong = song_listbox.get(next_index)
   song_title, artist_name = currentsong.split(" - ")

   if hasattr(play_pause_button, 'current_playlist'):
       if queue_text_label:
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
           pygame.mixer.music.load(file_path)
           pygame.mixer.music.play()
           song_length = MP3(file_path).info.length
       elif file_extension == ".wav":
           audio = AudioSegment.from_file(file_path, format="wav")
           pygame.mixer.music.load(file_path)
           pygame.mixer.music.play()
           song_length = len(audio) / 1000.0
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
                 progress_slider, queue_text_label, playlist_name, playlist_label, album_art_label, bottom_frame_left):   
   global currentsong, is_playing, current_song_position, song_length, song_start_time

   if song_listbox.size() == 0:
       print("The song list is empty!")
       return

   if not song_listbox.curselection():
       song_listbox.select_set(0)
       song_listbox.activate(0)
       current_index = (0,)
   else:
       current_index = song_listbox.curselection()

   previous_index = (current_index[0] - 1) % song_listbox.size()
   song_listbox.select_clear(0, END)
   song_listbox.select_set(previous_index)
   song_listbox.activate(previous_index)

   currentsong = song_listbox.get(previous_index)
   song_title, artist_name = currentsong.split(" - ")

   if hasattr(play_pause_button, 'current_playlist'):
       if queue_text_label:
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
           pygame.mixer.music.load(file_path)
           pygame.mixer.music.play()
           song_length = MP3(file_path).info.length
       elif file_extension == ".wav":
           audio = AudioSegment.from_file(file_path, format="wav")
           pygame.mixer.music.load(file_path)
           pygame.mixer.music.play()
           song_length = len(audio) / 1000.0
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