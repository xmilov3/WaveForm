import tkinter as tk
import pygame
from app.func.load_pic_gui import load_top_logo
from app.gui.panels.top_panel import create_top_panel
from app.gui.panels.left_panel import create_left_panel
from app.gui.panels.middle_panel import create_middle_panel
from app.gui.panels.right_panel import create_right_panel, update_next_in_queue, update_now_playing
from app.gui.panels.bottom_panel import create_bottom_panel
from app.func.music_controller import play_pause_song, stop_song, next_song, previous_song, initialize_first_song

pygame.mixer.init(channels=2)
pygame.mixer.music.stop()


class AppWindow(tk.Frame):
    def __init__(self, parent, page_manager, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.page_manager = page_manager
        self.configure(bg='#150016')

        self.main_frame = tk.Frame(self, bg='#150016')
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_panels()

    def init_panels(self):
        top_frame = create_top_panel(self.main_frame, self.page_manager)
        left_frame = create_left_panel(self.main_frame, self.page_manager)
        
        middle_frame, song_listbox = create_middle_panel(self.main_frame, "Liked Songs")

        right_frame, queue_text_label, playlist_label, album_art_label, title_label, artist_label = create_right_panel(
            self.main_frame, playlist_name="Liked Songs"
        )
        bottom_frame, time_remaining_label, time_elapsed_label, progress_slider, title_label, artist_label, play_pause_button, play_button_img, pause_button_img = create_bottom_panel(
            self.main_frame,
            song_listbox,
            queue_text_label,
            "Liked Songs",
            playlist_label,
            album_art_label,
            title_label,
            artist_label,
            update_next_in_queue,
            update_now_playing
        )

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
            bottom_frame
        )

        self.configure_layout(top_frame, left_frame, middle_frame, right_frame, bottom_frame)

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
