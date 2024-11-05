from tkinter import *
import customtkinter
import pygame
import os
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class MusicPlayer:
    current_song: Optional[str] = None
    is_playing: bool = False
    song_length: int = 0
    value: int = 0
    user_sliding: bool = False
    current_song_position: int = 0
    song_start_time: int = 0

class WaveFormApp:
    def __init__(self, root):
        self.root = root
        self.frames = {}
        #self.frames['bottom_center'] = customtkinter.CTkFrame(root)
        #self.frames['bottom_center'].pack(fill='x', padx=20, pady=10)
        self.setup_window()
        self.load_images()
        self.player = MusicPlayer()
        self.song_length = 0
        self.user_sliding = False
        #self.create_progress_bar()
        self.init_pygame()
        self.create_frames()
        self.setup_grid()
        self.create_widgets()
        self.load_songs()
        #self.update_progress_bar()
        
    # Main window            
    def setup_window(self):
        self.root.title("WaveForm")
        self.root.geometry("1500x1000")
        self.root.configure(bg='#2F033D')
    
    # Initiate pygame mixer
    def init_pygame(self):
        #pygame.mixer.init()
        pygame.mixer.init(channels=2, frequency=44100)
        
    # Background and icon images
    def load_images(self):
        images_base = Path('Pictures/')
        self.images = {
            'logo': PhotoImage(file=images_base / 'Logo.png'),
            'logo_top': PhotoImage(file=images_base / 'TopLogo.png'),
            'play_button': PhotoImage(file=images_base / 'play_button.png'),
            'pause_button': PhotoImage(file=images_base / 'pause_button.png'),
            'next_button': PhotoImage(file=images_base / 'next_button.png'),
            'previous_button': PhotoImage(file=images_base / 'previous_button.png')
        }
        self.root.iconphoto(False, self.images['logo'])
            
    def create_frames(self):
        self.main_frame = Frame(self.root, bg='black') # maybe right middle panel
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        
        frames = {
            # Top panel
            'top_panel': ('#032e3d', 0, 0, 3), #TOP PANEL APPROVED
            
            # Left panel
            'left_search': ('#033d1a', 1, 0, 1), # SEARCH PANNEL 
            'left_filters': ('#bfbf0b', 2, 0, 1), # LEFT BUTTONNS PANNEL
            'left_buttons': ('#3f85ba', 3, 0, 1),   # LEFT LIKED PLAYLIST PANNEL
            'bottom_left': ('#462691', 4, 0, 1), #NOT WORKING
            
            # Mid panel
            'main_header': ('#bfbf0b', 1, 1, 1), # PLAYLIST INFO
            'main_controls': ('#0d033d', 2, 1, 1), #MID CONTROL PANEL
            'main_song_list': ('#033d33', 3, 1, 1), # MID PLAYLIST
            'bottom_center': ('#032c3d', 4, 1, 1), # BOTTOM MID progress bar

            # Right panel
            'right_current_song': ('#0e3d03', 1, 2, 1), # NEXT IN QUEUE 
            'song_info': ('#2F033D', 2, 2, 1), #SONG INFO
            'right_queue': ('#22033d', 3, 2, 1), # RIGHT PANNEL DOWN
            'bottom_right': ('#032c3d', 4, 2, 3), #BOTTOM RIGHT

        
        }

        self.frames = {}
        for name, (bg, row, col, colspan) in frames.items():
            frame = Frame(self.main_frame, bg=bg)
            frame.grid(row=row, column=col, columnspan=colspan, sticky='nsew', padx=1, pady=1)
            self.frames[name] = frame
    # Configure grid weights
    def setup_grid(self):
    # Define the column weights to make the middle panel wider
        self.main_frame.grid_columnconfigure(0, weight=3)  # left panel (narrow)
        self.main_frame.grid_columnconfigure(1, weight=5)  # middle panel (wide)
        self.main_frame.grid_columnconfigure(2, weight=1)  # right panel (narrow)

    # Define row weights to make the top, middle, and bottom sections
        self.main_frame.grid_rowconfigure(0, weight=0)  # top panel (search bar)
        self.main_frame.grid_rowconfigure(1, weight=4)  # top of middle section (main header)
        self.main_frame.grid_rowconfigure(2, weight=1)  # mid of middle section (controls)
        self.main_frame.grid_rowconfigure(3, weight=5)  # main song list (primary content)
        self.main_frame.grid_rowconfigure(4, weight=0)  # filler row (for alignment, if needed)

    # Configure root window to expand with the main frame
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_widgets(self):
        self.create_top_widgets()
        self.create_left_widgets()
        self.create_middle_widgets()
        self.create_right_widgets()
        self.create_bottom_widgets()
    
    def create_top_widgets(self):
        logo_label = Label(self.frames['top_panel'], image=self.images['logo_top'], bg='#2F033D')
        logo_label.grid(row=0, column=1, sticky='e', padx=10, pady=5)
        
    def create_left_widgets(self):
        search_menu = Label(self.frames['left_search'], text="Search", font=("Arial", 14), fg='white', bg='#2F033D')
        search_menu.grid(row=2, column=1, sticky='nsew' )
        left_menu = Label(self.frames['left_filters'], text="Playlists", font=("Arial", 14), fg='white', bg='#2F033D')
        Button(self.frames['left_filters'], text="Filters", font=("Arial", 14), fg='white', bg='#2F033D')
        Button(self.frames['left_buttons'], text="Add Song", font=("Arial", 14), fg='red', bg='white')
        Button(self.frames['left_buttons'], text="Analyze Song", font=("Arial", 14), fg='red', bg='white')
        
        left_menu.grid(row=1, column=0, sticky='nsew', padx=1, pady=1)
        Label(self.frames['bottom_left'], text="Playlists", font=("Arial", 14), fg='yellow', bg='#2F033D')
        Button(self.frames['bottom_left'], text="Liked Songs", font=("Arial", 14), fg='#1E052A', bg='white')
        Button(self.frames['bottom_left'], text="UK Bassline", font=("Arial", 14), fg='#1E052A', bg='white')

    def create_middle_widgets(self):
        Label(self.frames['main_header'], text="Header", font=("Arial", 14), fg='gray', bg='#2F033D')
        Label(self.frames['main_controls'], text="Controls", font=("Arial", 14), fg='gray', bg='#2F033D')
        Label(self.frames['main_song_list'], text="Song List", font=("Arial", 14), fg='gray', bg='#2F033D')
        self.song_listbox = Listbox(self.frames['main_song_list'], bg='#2F033D', fg='white', height=15, width=40)
        self.song_listbox.pack(padx=10, pady=5)
              
    def create_right_widgets(self):
        Label(self.frames['right_current_song'], text="Current Song", font=("Arial", 14), fg='gray', bg='#2F033D')
        self.now_playing_label = Label(self.frames['right_current_song'], text="No song playing", font=("Arial", 14), fg='white', bg='#2F033D')
        Label(self.frames['song_info'], text="Song Info", font=("Arial", 14), fg='gray', bg='#2F033D')
        Label(self.frames['right_queue'], text="Queue", font=("Arial", 14), fg='gray', bg='#2F033D')
    
    def create_bottom_widgets(self):
        self.create_now_playing_song()
        self.create_playback_controls()
        self.create_progress_bar()
        self.create_volume_controls()
        
    def create_now_playing_song(self):
        Label(self.frames['bottom_left'], text="Now Playing", font=("Arial", 14), fg='gray', bg='#2F033D')
        self.title_label = Label(self.frames['bottom_left'], font=("Arial", 14), bg='#2F033D')
        self.artist_label = Label(self.frames['bottom_left'], font=("Arial", 14), bg='#2F033D')
        self.title_label.pack()
        self.artist_label.pack()
        
    def create_playback_controls(self):
        controls_frame = Frame(self.frames['bottom_center'], bg='#2F033D')
        controls_frame.pack(fill='x', pady=10)
        
        for image_key, command in [
            ('previous_button', self.previous_song),
            ('play_button', self.play_pause_song),
            ('next_button', self.next_song)
        ]:
            label = Label(controls_frame, image=self.images[image_key], bg='#2F033D')
            label.pack(side='left', padx=10)
            label.bind('<Button-1>', command)
            if image_key == 'play_button':
                self.play_pause_label = label
    
    def create_progress_bar(self):
        self.time_elapsed_label = customtkinter.CTkLabel(self.frames['bottom_center'], text="00:00")
        self.time_remaining_label = customtkinter.CTkLabel(self.frames['bottom_center'], text="-00:00")

        self.progress_slider = customtkinter.CTkSlider(self.frames['bottom_center'], from_=0, to=100, command=self.slide_music)
        #self.progress_slider.set(0)
        self.time_elapsed_label.pack(side='left')
        self.progress_slider.pack(side='left', fill='x', expand=True)
        self.time_remaining_label.pack(side='left')
        
    def create_volume_controls(self):
        self.volume_label = customtkinter.CTkLabel(self.frames['bottom_right'], text="Volume: 100%")
        self.volume_bar = customtkinter.CTkSlider(self.frames['bottom_right'], from_=0, to=100, command=self.control_volume)
        self.volume_bar.set(100)
        self.volume_label.pack(pady=20)
        self.volume_bar.pack(pady=10, padx=10, fill="x")
        
    def load_songs(self):
        self.song_listbox.delete(0, END)
        self.music_dir = Path('Music/')
        
        supported_formats = ('.mp3', '.wav')
        songs=[]
        for format in supported_formats:
            songs.extend(self.music_dir.glob(f'*{format}'))
            
        songs.sort()
        
        for song in songs:
            self.song_listbox.insert(END, song.name)
            
    def get_song_length(self, song_path):
        if song_path.suffix.lower() == '.mp3':
            sound = pygame.mixer.Sound(str(song_path))
            return int(sound.get_length())
        else:
            import wave
            with wave.open(str(song_path), 'rb') as wav_file:  
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                return int(frames / float(rate))      
    
            # Manipulate song functions
    def play_pause_song(self, event=None):
        if not self.song_listbox.curselection():
            return

        selected_song = self.song_listbox.get(ACTIVE)
        song_path = self.music_dir / selected_song

        if self.player.is_playing and selected_song == self.player.current_song:
            # If the song is already playing, pause it
            pygame.mixer.music.pause()
            self.play_pause_label.config(image=self.images['play_button'])
            self.player.is_playing = False  # Update state to not playing
        else:
            if selected_song != self.player.current_song:
                # If a different song is selected, load and play it
                try:
                    pygame.mixer.music.load(str(song_path))
                    pygame.mixer.music.play()
                    self.player.song_length = self.get_song_length(song_path)
                    self.player.current_song = selected_song
                    self.player.current_song_position = 0  # Reset position for new song
                    self.update_now_playing()  # Update UI to show the current song
                    self.update_progress_bar()  # Reset progress bar to the new song
                except Exception as e:
                    print(f"Error trying to play: {e}")
                    self.now_playing_label.config(text=f"Error: {selected_song}")
                    return
            else:
            # If the same song is selected again, just unpause it
                pygame.mixer.music.unpause()
        
        self.play_pause_label.config(image=self.images['pause_button'])
        self.player.is_playing = True  # Update state to playing

                

            
    def next_song(self, event=None):
        if not self.song_listbox.curselection():
            return
        current_index = self.song_listbox.curselection()[0]
        next_index = (current_index + 1) % self.song_listbox.size()
        self.change_song(next_index)
        
        
    def previous_song(self, event=None):
        if not self.song_listbox.curselection():
            return
        current_index = self.song_listbox.curselection()[0]
        previous_index = (current_index - 1) % self.song_listbox.size()
        self.change_song(previous_index)
    
    def change_song(self, index):
        self.song_listbox.select_clear(0, END)
        self.song_listbox.select_set(index)
        self.song_listbox.activate(index)
        self.player.is_playing = False
        self.play_pause_song()
        
        
    def update_now_playing(self):
        if not self.player.current_song:
            return
        
        song_name = str(self.player.current_song)
        for ext in ['.mp3', '.wav']:
            song_name = song_name.replace(ext, '')
            
        # if " - " in song_name:
        #     artist, title = song_name.split(" - ")
        #     title = title[:20] + '...' if len(title) > 20 else title
        #     artist = artist[:20] + '...' if len(artist) > 20 else artist
        #     self.title_label.config(text=f"{title}")
        #     self.artist_label.config(text=f"{artist}")
        # else:
        display_text = song_name[:40] + "..." if len(song_name) > 40 else song_name
        self.now_paying_label.config(text=display_text)
        
    def control_volume(self, value):
        pygame.mixer.music.set_volume(float(value)/100)
        self.volume_label.configure(text=f"Volume: {int(value)}%")

    def update_progress(self):
        #global current_song_position
    
        if not self.player.user_sliding and self.player.is_playing:
            current_time_ms = pygame.mixer.music.get_pos() // 1000
            if current_time_ms >= 0:  # Check if music is playing
                self.player.current_song_position = int(current_time_ms / 1000) + self.player.song_start_time
                remaining_time = self.player.song_length - current_time_ms
                #- self.player.current_song_position
                #current_song_position = int(current_time_ms / 1000) + self.song_start_time

                self.time_elapsed_label.configure(
                    text=f"{current_time_ms//60:02d}:{current_time_ms%60:02d}"
                )
                self.time_remaining_label.configure(
                    text=f"-{remaining_time//60:02d}:{remaining_time%60:02d}"
                )
                
            #self.time_elapsed_label.configure(text=time.strftime("%M:%S", time.gmtime(self.player.current_song_position)))
            #self.time_remaining_label.configure(text=time.strftime("-%M:%S", time.gmtime(remaining_time)))

                if self.player.song_length > 0:
                    self.progress_slider.set((current_time_ms / self.player.song_length) * 100)
                
        if pygame.mixer.music.get_busy() or self.player.is_playing:
            self.root.after(1000, self.update_progress)
  
        
    



    def slide_music(self, value):
       if not self.player.current_song:
           return
       
       self.player.user_sliding = True
       new_time = (float(value) / 100) * self.player.song_length
       
       
       song_path = self.music_dir  / self.player.current_song
       pygame.mixer.music.load(song_path)
       pygame.mixer.music.play(start=new_time)
       self.root.after(500, lambda: setattr(self.player, 'user_sliding', False))
    #self.user_sliding = True
        
        # Calculate the new time position based on slider value
    #new_time = (float(value) / 100) * self.song_length
        
        # Stop and start playback at the new position
    #pygame.mixer.music.stop()
    #pygame.mixer.music.play(start=new_time)
        
        # Update song position
    #self.current_song_position = new_time
    #self.update_time_labels(new_time)
        
        # Set user_sliding to False after a short delay
    #self.root.after(500, lambda: self.set_user_sliding(False))
    
#def set_user_sliding(value):
    #global user_sliding
    #user_sliding = value



if  __name__ == "__main__":
    root = Tk()
    app = WaveFormApp(root)
    root.mainloop()

