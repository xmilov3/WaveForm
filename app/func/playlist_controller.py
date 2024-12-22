import pygame
from app.db.database import create_connection
from tkinter import messagebox
from app.func.music_controller import initialize_first_song
from app.func.shared_func import play_playlist


pygame.mixer.init()

def play_playlist(playlist_name, song_listbox, play_pause_button, play_button_img, pause_button_img, 
                  title_label, artist_label, time_elapsed_label, time_remaining_label, 
                  progress_slider, bottom_frame):
    initialize_first_song(
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
        playlist_name
    )


def play_song(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print(f"Playing: {file_path}")
    except Exception as e:
        print(f"Error playing song: {e}")

def stop_music():
    try:
        pygame.mixer.music.stop()
        print("Music stopped.")
    except Exception as e:
        print(f"Error stopping music: {e}")

def pause_music():
    try:
        pygame.mixer.music.pause()
        print("Music paused.")
    except Exception as e:
        print(f"Error pausing music: {e}")

def unpause_music():
    try:
        pygame.mixer.music.unpause()
        print("Music resumed.")
    except Exception as e:
        print(f"Error resuming music: {e}")
