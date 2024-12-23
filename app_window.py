import tkinter as tk
import pygame
from app.func.load_pic_gui import load_top_logo
from app.gui.panels.top_panel import create_top_panel
from app.gui.panels.left_panel import create_left_panel
from app.gui.panels.middle_panel import create_middle_panel
from app.gui.panels.right_panel import create_right_panel, update_next_in_queue, update_now_playing
from app.gui.panels.bottom_panel import create_bottom_panel
from app.func.music_controller import play_pause_song, stop_song, next_song, previous_song, initialize_first_song, sync_is_playing, create_song_listbox
from app.func.playlist_utils import fetch_playlists, update_playlist_buttons
from app.gui.panels.left_panel import populate_playlists
from mutagen.mp3 import MP3
from pydub import AudioSegment
import mysql.connector
import os
import time

pygame.mixer.init(channels=2)
pygame.mixer.music.stop()

currentsong = None
song_length = 0
current_song_position = 0
song_start_time = 0
is_playing = False


class AppWindow(tk.Frame):
    def __init__(self, parent, page_manager, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.page_manager = page_manager
        self.configure(bg='#150016')
        self.main_frame = tk.Frame(self, bg='#150016')
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.delete_playlist_callback = self.delete_playlist
        self.change_cover_callback = self.change_playlist_cover

        self.init_panels()

        populate_playlists(self.left_panel.playlist_frame, self.page_manager)

    def delete_playlist(self, playlist_name):
        print(f"Deleting playlist: {playlist_name}")

    def change_playlist_cover(self, playlist_name):
        print(f"Changing cover for playlist: {playlist_name}")

    def init_panels(self):
        playlists = fetch_playlists()
        first_playlist = playlists[0] if playlists else "Unknown Playlist"

        self.middle_panel, self.header_frame, self.songlist_frame, self.song_listbox = create_middle_panel(
            self.main_frame, first_playlist
        )
        
        self.top_panel = create_top_panel(self.main_frame, self.page_manager)

        playlists = fetch_playlists()
        first_playlist = playlists[0] if playlists else "Unknown Playlist"


        self.right_panel, self.queue_text_label, self.playlist_label, self.album_art_label, self.title_label, self.artist_label = create_right_panel(
            self.main_frame, playlist_name=first_playlist
        )

        self.bottom_panel, self.time_remaining_label, self.time_elapsed_label, self.progress_slider, self.title_label, self.artist_label, self.play_pause_button, self.play_button_img, self.pause_button_img = create_bottom_panel(
            self.main_frame,
            self.song_listbox,
            self.queue_text_label,
            first_playlist,
            self.playlist_label,
            self.album_art_label,
            self.title_label,
            self.artist_label,
            update_next_in_queue,
            update_now_playing,
        )

        self.left_panel = create_left_panel(
            self.main_frame,
            self.page_manager,
            self.song_listbox,
            self.play_pause_button,
            self.play_button_img,
            self.pause_button_img,
            self.title_label,
            self.artist_label,
            self.time_elapsed_label,
            self.time_remaining_label,
            self.progress_slider,
            self.bottom_panel,
            self.delete_playlist_callback,
            self.change_cover_callback
        )

        self.configure_layout(self.top_panel, self.left_panel, self.middle_panel, self.right_panel, self.bottom_panel)



        self.song_listbox.bind("<Double-Button-1>", lambda event: self.select_song_from_list())

        self.start_sync_loop()

    def select_song_from_list(self):
        global currentsong
        selected_index = self.song_listbox.curselection()
        if not selected_index:
            print("No song selected!")
            return

        currentsong = self.song_listbox.get(selected_index)
        self.load_song(currentsong)

    def load_song(self, song_info):
        global currentsong, song_length, current_song_position, song_start_time, is_playing

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

            self.play_pause_button.config(image=self.play_button_img) 
            self.time_elapsed_label.config(text="00:00")
            self.time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(song_length)))
            self.progress_slider.set(0)
            self.title_label.config(text=song_title)
            self.artist_label.config(text=artist_name)

            currentsong = song_info
            is_playing = False
            current_song_position = 0
            song_start_time = 0

            print(f"Loaded song: {song_title} - {artist_name}")

        except Exception as e:
            print(f"Error in load_song: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def start_sync_loop(self):
        global is_playing, current_song_position, song_start_time, song_length

        if is_playing:
            current_time = pygame.mixer.music.get_pos() / 1000.0 + song_start_time
            self.time_elapsed_label.config(text=time.strftime("%M:%S", time.gmtime(current_time)))
            remaining_time = song_length - current_time
            self.time_remaining_label.config(text=time.strftime("-%M:%S", time.gmtime(remaining_time)))
            self.progress_slider.set((current_time / song_length) * 100)

        self.after(500, self.start_sync_loop)
    

    def configure_layout(self, top_frame, left_frame, middle_frame, right_frame, bottom_frame):
        # Main Frame
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=5)
        self.main_frame.grid_columnconfigure(2, weight=2)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=4)
        self.main_frame.grid_rowconfigure(2, weight=0)

        # Top Frame
        top_frame.grid_columnconfigure(0, weight=1)

        # Left Frame
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=10)
        left_frame.grid_columnconfigure(0, weight=1)

        # Middle Frame
        middle_frame.grid_rowconfigure(0, weight=1)
        middle_frame.grid_rowconfigure(1, weight=3)
        middle_frame.grid_columnconfigure(0, weight=1)

        # Right Frame
        right_frame.grid_rowconfigure(0, weight=5)
        right_frame.grid_rowconfigure(1, weight=4)
        right_frame.grid_columnconfigure(0, weight=1)

        # Bottom Frame
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_rowconfigure(1, weight=0)
        bottom_frame.grid_rowconfigure(2, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=3)
        bottom_frame.grid_columnconfigure(1, weight=6)
        bottom_frame.grid_columnconfigure(2, weight=1)
