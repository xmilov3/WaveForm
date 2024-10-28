from tkinter import *
import customtkinter
import pygame
import os
import time 

# Main window            
root = Tk()
root.title("WaveForm")
root.geometry("1500x1000")
root.configure(bg='#1E052A')

# Initiate pygame mixer
pygame.mixer.init()
pygame.mixer.init(channels=2)

# Main pannel
main_frame = Frame(root, bg='black')
main_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
# Top pannel
top_frame = Frame(main_frame, bg='#1E052A')
top_frame.grid(row=0, column=0, columnspan=3, sticky='ew', padx=1, pady=1)
#Left pannel
left_frame = Frame(main_frame, bg='#240745')
left_frame.grid(row=1, column=0, sticky='nsew', padx=1, pady=1)
# Mid pannel
middle_frame = Frame(main_frame, bg='#3C0F64')
middle_frame.grid(row=1, column=1, sticky='nsew', padx=1, pady=1)


# Right pannel
right_frame = Frame(main_frame, bg='#3A0C60')
right_frame.grid(row=1, column=2, sticky='nsew', padx=1, pady=1)

#  Bottom left pannel
bottom_frame_left = Frame(main_frame, bg='#1E052A')
bottom_frame_left.grid(row=2, column=0, sticky='nsew', padx=1, pady=1)


# Bottom midlle panel
bottom_frame_mid = Frame(main_frame, bg='#1E052A')
bottom_frame_mid.grid(row=2, column=1, sticky='nsew', padx=1, pady=1)

# Bottom right panel
bottom_frame_right = Frame(main_frame, bg='#1E052A')
bottom_frame_right.grid(row=2, column=2, sticky='ew', padx=1, pady=1)

# Widgets
bottom_left_widget = Label(bottom_frame_left, bg='#1E052A')
bottom_left_widget.grid(row=0, column=0, sticky='nsew')
bottom_left_widget.pack(padx=1, pady=10)
# Bottom center widget
bottom_center_widget = Label(bottom_frame_mid, bg='#1E052A')
bottom_center_widget.grid(row=0, column=1, sticky='ew')
bottom_center_widget.pack(padx=1, pady=10)

# Background and icon images
img = PhotoImage(file='../WaveForm/Pictures/Logo.png')
logo_top = PhotoImage(file='../WaveForm/Pictures/TopLogo.png')
play_button = PhotoImage(file='../WaveForm/gui/buttons/play_button.png')
pause_button = PhotoImage(file='../WaveForm/gui/buttons/pause_button.png')
next_button = PhotoImage(file='../WaveForm/gui/buttons/next_button.png')
previous_button = PhotoImage(file='../WaveForm/gui/buttons/previous_button.png')
root.iconphoto(False, img)


# Grid settings

main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_rowconfigure(2, weight=0)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=3)
main_frame.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
logo_label = Label(top_frame, image=logo_top, bg='#1E052A')
logo_label.grid(row=0, column=1, sticky='e', padx=10, pady=5)
Label(top_frame, bg='#1E052A').grid(row=0, column=0, sticky='w')
top_frame.grid_columnconfigure(0, weight=1)

# Playlist page grid
middle_frame.grid_rowconfigure(1,  weight=1)
middle_frame.grid_rowconfigure(2,  weight=1)
middle_frame.grid_rowconfigure(3,  weight=1)

# Bottom frame grid
bottom_frame_mid.grid_columnconfigure(0, weight=1)
bottom_frame_mid.grid_columnconfigure(1, weight=1)
bottom_frame_mid.grid_columnconfigure(2, weight=1)

# Window and label width


# Labels

# Left frame labels
Label(left_frame, text="Playlists", font=("Arial", 14), fg='white', bg='#240745').pack(pady=5)
playlist1 = Button(left_frame, text="Liked songs", width=20, height=2, fg='black', bg='red')
playlist1.pack(pady=5)
playlist2 = Button(left_frame, text="UK Dubstep", width=20, height=2, fg='black', bg='black')
playlist2.pack( pady=5)

# Right frame labels
Label(right_frame, text="Now Playing", font=("Arial", 14), fg='white', bg='#3A0C60').pack(pady=5)
right_frame = Label(right_frame, font=("Arial", 12), fg='white', bg='#3A0C60')
#right_frame.bind("<Button-1>", now_playing)

# Middle frame labels
Label(middle_frame, text='Playlist: UK Bassline', font=("Arial", 14), fg='white', bg='#3C0F64').pack(pady=5)
song_listbox = Listbox(middle_frame, bg='#1E052A', fg='white', height=15, width=40)
song_listbox.pack(padx=10, pady=5)




# Now songs are static, in future they will be dynamic
os.chdir('../WaveForm/Music')
songs = os.listdir()
for s in songs:
    song_listbox.insert(END, s)
    
# Global variables
global is_playing, current_song_position, song_start_time
is_playing = False
global song_length
song_length = 0
global user_sliding 
user_sliding = False
current_song_position = 0
song_start_time = 0


# Manipulate song functions
def play_pause_song(event=None):
    global is_playing, song_length, current_song_position, song_start_time
    currentsong = song_listbox.get(ACTIVE)
    if is_playing:
        pygame.mixer.music.pause()
        play_pause_label.config(image=play_button)
    else:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(currentsong)
            current_song_position = 0
            song_start_time = 0
            pygame.mixer.music.play()
            song_length = int(pygame.mixer.Sound(currentsong).get_length())
            now_playing()
            progress_bar()
        else:
            pygame.mixer.music.unpause()
            now_playing()
        play_pause_label.config(image=pause_button)
    is_playing = not is_playing
    
def stop_song():
    global is_playing
    pygame.mixer.music.stop()
    play_pause_label.config(image=play_button)
    is_playing = False
    
def next_song(event=None):
    global is_playing
    stop_song()
    current_index = song_listbox.curselection()[0]
    next_index = (current_index + 1) % song_listbox.size()
    song_listbox.select_clear(0, END)
    song_listbox.select_set(next_index)
    song_listbox.activate(next_index)
    play_pause_song()
    
def previous_song(event=None):
    global is_playing
    stop_song()
    current_index = song_listbox.curselection()[0]
    previous_index = (current_index - 1) % song_listbox.size()
    song_listbox.select_clear(0, END)
    song_listbox.select_set(previous_index)
    song_listbox.activate(previous_index)
    play_pause_song()
    
# Display current playing song
def now_playing():
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
       # right_frame.config(text=f"{title} - {artist}")
    else:
        currentsong_display = currentsong[:20] + "..." if len(currentsong) > 20 else currentsong
        title_label.config(text=f"{currentsong_display}")
        artist_label.config(text=f"{currentsong_display}")
       # right_frame.config(text=f"{currentsong_display}")
        
    
def control_volume(value):
    pygame.mixer.music.set_volume(float(value)/100)
    volume_label.configure(text=f"Volume: {int(value)}%")

def progress_bar():
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
        bottom_center_widget.after(1000, progress_bar)

def slide_music(value):
    global user_sliding, current_song_position, song_start_time
    user_sliding = True
    new_time = (float(value) / 100) * song_length
    
    pygame.mixer.music.stop()
    pygame.mixer.music.play(start=new_time)
    song_start_time = new_time  # Store the start time for get_pos() calculations
    current_song_position = new_time
    
    time_elapsed_label.configure(text=time.strftime("%M:%S", time.gmtime(new_time)))
    time_remaining_label.configure(text=time.strftime("-%M:%S", time.gmtime(song_length - new_time)))
    
    bottom_center_widget.after(500, lambda: set_user_sliding(False))

    
def set_user_sliding(value):
    global user_sliding
    user_sliding = value

def create_widgets(self):
    self.create_bottom_widgets()
    
def create_bottom_widgets(self):
    self.create_
# Bottom left frame labels

title_label = Label(bottom_left_widget, fg="white",  bg='#1E052A', font=("Arial", 18, "bold"))
title_label.pack(side=TOP, padx=0, pady=5)
title_label.bind("<Button-1>", now_playing)

artist_label = Label(bottom_left_widget, fg="white",  bg='#1E052A', font=("Arial", 14, "bold"))
artist_label.pack(side=TOP, padx=7, pady=5)
title_label.bind("<Button-1>", now_playing)


# Bottom center frame labels

previous_label = Label(bottom_center_widget, image=previous_button, bg='#1E052A')
previous_label.pack(side="left", padx=10)
previous_label.bind("<Button-1>", previous_song)

play_pause_label = Label(bottom_center_widget, image=play_button, bg='#1E052A')
play_pause_label.pack(side="left", padx=10)
play_pause_label.bind("<Button-1>", play_pause_song)

next_label = Label(bottom_center_widget, image=next_button, bg='#1E052A')
next_label.pack(side="left", padx=10)
next_label.bind("<Button-1>", next_song)

time_elapsed_label = customtkinter.CTkLabel(bottom_center_widget, text="00:00")
time_elapsed_label.pack(side="right", padx=10)

progress_slider = customtkinter.CTkSlider(bottom_center_widget, from_=0, to=100, command=slide_music)
progress_slider.set(0)
progress_slider.pack(side="right", pady=20, padx=20, fill="x")

time_remaining_label = customtkinter.CTkLabel(bottom_center_widget, text="-00:00")
time_remaining_label.pack(side="right", padx=10)


# Bottom right frame labels

#Volume bar
volume_label = customtkinter.CTkLabel(bottom_frame_right, text="Volume: 100%")
volume_label.pack(pady=20)

volume_bar = customtkinter.CTkSlider(bottom_frame_right, from_=0, to=100, command=control_volume)

volume_bar.set(100)
volume_bar.pack(pady=10, padx=10, fill="x")


root.mainloop()
