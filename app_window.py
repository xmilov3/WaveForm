import tkinter as tk
from tkinter import messagebox, Listbox, BOTH, SINGLE, END
from app.func.config import *
import pygame
from app.func.load_pic_gui import load_top_logo
from app.gui.panels.top_panel import create_top_panel
from app.gui.panels.left_panel import create_left_panel
from app.gui.panels.middle_panel import create_middle_panel
from app.gui.panels.right_panel import create_right_panel, update_next_in_queue, update_now_playing
from app.gui.panels.bottom_panel import create_bottom_panel
from app.func.music_controller import play_pause_song, stop_song, next_song, previous_song, initialize_first_song, sync_is_playing, populate_song_listbox, progress_bar, play_selected_song, load_song, set_current_song_by_index

from app.func.playlist_utils import fetch_playlists
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


        self.title_label = tk.Label(self.main_frame, text="Title", bg="#1E052A", fg="white")
        self.artist_label = tk.Label(self.main_frame, text="Artist", bg="#1E052A", fg="white")
        self.time_elapsed_label = tk.Label(self.main_frame, text="00:00", bg="#1E052A", fg="white")
        self.time_remaining_label = tk.Label(self.main_frame, text="-00:00", bg="#1E052A", fg="white")
        self.progress_slider = tk.Scale(self.main_frame, from_=0, to=100, orient="horizontal", bg="#1E052A", fg="white")

        playlists = fetch_playlists()
        self.first_playlist = playlists[0] if playlists else "Unknown Playlist"

        

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_panels()
        populate_playlists(self.left_panel.playlist_frame, self.page_manager)

    def init_panels(self):
        

        (
            self.right_panel,
            self.queue_text_label,
            self.playlist_label,
            self.album_art_label,
            self.title_label,
            self.artist_label
        ) = create_right_panel(
            self.main_frame, 
            playlist_name=self.first_playlist
            )

        (
            self.middle_panel,
            self.header_frame,
            self.songlist_frame,
            self.song_listbox
        ) = create_middle_panel(
            parent=self.main_frame,
            playlist_name=self.first_playlist,
            title_label=self.title_label,
            artist_label=self.artist_label,
            album_art_label=None,
            time_elapsed_label=self.time_elapsed_label,
            time_remaining_label=self.time_remaining_label,
            progress_slider=self.progress_slider
        )

        (
            self.bottom_panel,
            self.time_remaining_label,
            self.time_elapsed_label,
            self.progress_slider,
            self.play_pause_button,
            self.play_button_img,
            self.pause_button_img,
        ) = create_bottom_panel(
            self.main_frame,
            self.song_listbox,
            None,  # self.queue_label
            self.first_playlist,
            None,  # self.playlist_label
            None,  # self.album_label
            self.title_label,
            self.artist_label,
            update_next_in_queue,
            update_now_playing
        )


        if self.song_listbox:
            self.song_listbox.bind("<Double-Button-1>", lambda event: self.select_song_from_list())
        else:
            print("Error: song_listbox is not initialized.")

        self.top_panel = create_top_panel(self.main_frame, self.page_manager)

        self.left_panel = create_left_panel(
            self.main_frame,
            self.page_manager
        )
        

        self.configure_layout(self.top_panel, self.left_panel, self.middle_panel, self.right_panel, self.bottom_panel)

        update_next_in_queue(self.queue_text_label, self.first_playlist)
        update_now_playing(self.playlist_label, self.album_art_label, self.title_label, self.artist_label, self.first_playlist)

        self.start_sync_loop()

    def set_current_song_by_index(song_listbox, index):
        global currentsong
        if song_listbox.size() == 0:
            print("No songs in the playlist!")
            return None

        if index < 0 or index >= song_listbox.size():
            print(f"Invalid song index: {index}")
            return None

        song_listbox.select_clear(0, END)
        song_listbox.select_set(index)
        song_listbox.activate(index)
        currentsong = song_listbox.get(index)
        print(f"Set current song: {currentsong} (index: {index})")
        return currentsong


    def delete_playlist(self, playlist_name):
        print(f"Deleting playlist: {playlist_name}")

    def change_playlist_cover(self, playlist_name):
        print(f"Changing cover for playlist: {playlist_name}")
        
    def on_playlist_select(self, event):
        selected_index = event.widget.curselection()
        if not selected_index:
            return

        selected_playlist = event.widget.get(selected_index[0])
        print(f"Selected playlist: {selected_playlist}")

        

    def select_song_from_list(self):
        selected_index = self.song_listbox.curselection()
        if not selected_index:
            print("No song selected!")
            return

        self.song_listbox.select_clear(0, END)
        self.song_listbox.select_set(selected_index[0])
        self.song_listbox.activate(selected_index[0])


        selected_song = self.song_listbox.get(selected_index)
        global currentsong
        currentsong = selected_song
        print(f"Activated song index: {selected_index[0]}")
        play_selected_song(
            selected_song,
            self.title_label,
            self.artist_label,
            self.album_art_label,
            self.time_elapsed_label,
            self.time_remaining_label,
            self.progress_slider
        )
        update_now_playing(
        self.playlist_label,
        self.album_art_label,
        self.title_label,
        self.artist_label,
        self.first_playlist
    )




    def change_playlist(self, new_playlist_name):
        print(f"Changing playlist to: {new_playlist_name}")

        populate_song_listbox(self.song_listbox, new_playlist_name)

        if hasattr(self.bottom_panel, "update_song_listbox"):
            self.bottom_panel.update_song_listbox(self.song_listbox)

        if self.song_listbox.size() > 0:
            print("Playlist is not empty. Setting first song as active.")
            currentsong = set_current_song_by_index(self.song_listbox, 0)
            if currentsong:
                play_selected_song(
                    currentsong,
                    self.title_label,
                    self.artist_label,
                    self.album_art_label,
                    self.time_elapsed_label,
                    self.time_remaining_label,
                    self.progress_slider
                )
                update_now_playing(
                self.playlist_label,
                self.album_art_label,
                self.title_label,
                self.artist_label,
                new_playlist_name
            )
        else:
            print("Playlist is empty.")
            currentsong = None
            self.title_label.config(text="Title")
            self.artist_label.config(text="Artist")
            self.time_elapsed_label.config(text="00:00")
            self.time_remaining_label.config(text="-00:00")

    def on_song_double_click(self, event):
        selected_index = self.song_listbox.curselection()
        if not selected_index:
            print("No song selected!")
            return

        self.song_listbox.select_clear(0, END)
        self.song_listbox.select_set(selected_index[0])
        self.song_listbox.activate(selected_index[0])

        song_info = self.song_listbox.get(selected_index[0])
        print(f"Activated song index: {selected_index[0]}, song info: {song_info}")

        play_selected_song(
            song_info,
            self.title_label,
            self.artist_label,
            self.album_art_label,
            self.time_elapsed_label,
            self.time_remaining_label,
            self.progress_slider
        )

        

    def start_sync_loop(self):
        if is_playing:
            current_time = pygame.mixer.music.get_pos() / 1000.0 + song_start_time
            self.time_elapsed_label.config(text=time.strftime("%M:%S", time.gmtime(current_time)))
            remaining_time = song_length - current_time
            self.time_remaining_label.config(text=f"-{time.strftime('%M:%S', time.gmtime(remaining_time))}")
            self.progress_slider.set((current_time / song_length) * 100)

        self.after(500, self.start_sync_loop)

    def configure_layout(self, top_frame, left_frame, middle_frame, right_frame, bottom_frame):
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=5)
        self.main_frame.grid_columnconfigure(2, weight=2)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=4)
        self.main_frame.grid_rowconfigure(2, weight=0)

        top_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=10)
        left_frame.grid_columnconfigure(0, weight=1)
        middle_frame.grid_rowconfigure(0, weight=1)
        middle_frame.grid_rowconfigure(1, weight=3)
        middle_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=5)
        right_frame.grid_rowconfigure(1, weight=4)
        right_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_rowconfigure(1, weight=0)
        bottom_frame.grid_rowconfigure(2, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=3)
        bottom_frame.grid_columnconfigure(1, weight=6)
        bottom_frame.grid_columnconfigure(2, weight=1)
