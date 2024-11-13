from tkinter import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image, ImageTk
# from get_cover_art import CoverFinder
import customtkinter
import pygame
import os
import time
import io

# Main window            
root = Tk()
root.title("WaveForm")
root.geometry("1500x1000")
root.configure(bg='#1E052A')

# Global variables
global is_playing, current_song_position, song_start_time
is_playing = False
global song_length
song_length = 0
global user_sliding 
user_sliding = False
current_song_position = 0
song_start_time = 0

# Initiate pygame mixer
pygame.mixer.init()
pygame.mixer.init(channels=2)


# Trying new idea
# finder = CoverFinder(OPTIONS=songs)
# finder.scan_folder()

# Main pannel
main_frame = Frame(root, bg='black')
main_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
# Top pannel
top_frame = Frame(main_frame, bg='#1E052A')
top_frame.grid(row=0, column=0, columnspan=3, sticky='ew', padx=1, pady=1)
#Left pannel
left_frame = Frame(main_frame, bg='#3A0C60')
left_frame.grid(row=1, column=0, sticky='nsew', padx=1, pady=1)
search_frame = Frame(left_frame, bg='#3A0C60')
search_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
search_type_frame = Frame(search_frame, bg='#3A0C60')
search_type_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
search_buttons_frame = Frame(search_frame, bg='blue')
search_buttons_frame.grid(row=1, column=0, sticky='nsew', padx=1, pady=1)
pinned_playlist_frame = Frame(left_frame, bg='red')
pinned_playlist_frame.grid(row=1, column=0, sticky='nsew', padx=1, pady=1)
# Mid pannel
middle_frame = Frame(main_frame, bg='#3C0F64')
middle_frame.grid(row=1, column=1, sticky='nsew', padx=1, pady=1)
header_frame = Frame(middle_frame, bg='#3A0C60')
header_frame.grid(row=0, columnspan=3, sticky='nsew', padx=1, pady=1)
songlist_frame = Frame(middle_frame, bg='black')
songlist_frame.grid(row=1, columnspan=3, sticky='nsew', padx=1, pady=1)
# Right pannel
right_frame = Frame(main_frame, bg='#3A0C60')
right_frame.grid(row=1, column=2, sticky='nsew', padx=1, pady=1)
now_playing_frame = Frame(right_frame, bg='#3A0C60')
now_playing_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
now_playing_frame.place(relx=0.5, rely=0.06, anchor=CENTER)
next_in_queue_frame = Frame(right_frame, bg='#3C0F64')
next_in_queue_frame.grid(row=1, column=0, sticky='nsew', padx=1, pady=1)
#  Bottom left pannel
bottom_frame_left = Frame(main_frame, bg='#1E052A')
bottom_frame_left.grid(row=2, column=0, sticky='nsew', pady=1)
# Bottom midlle panel
bottom_frame_mid = Frame(main_frame, bg='#1E052A')
bottom_frame_mid.grid(row=2, column=1, sticky='nsew', pady=1)

# Bottom right panel
bottom_frame_right = Frame(main_frame, bg='#1E052A')
bottom_frame_right.grid(row=2, column=2, sticky='ew', pady=1)

# Widgets
bottom_left_widget = Label(bottom_frame_left, bg='#1E052A')
bottom_left_widget.grid(row=0, column=0, sticky='nsew')
bottom_left_widget.pack(pady=1)
# Bottom center widget
bottom_center_widget = Label(bottom_frame_mid, bg='#1E052A')
bottom_center_widget.grid(row=1, column=1, sticky='nsew', padx=50)
bottom_center_widget.place(relx=0.5, rely=0.4, anchor=CENTER)
bottom_center_bar = Label(bottom_frame_mid, bg='#1E052A')
bottom_center_bar.grid(row=2, column=1, sticky='nsew')
#bottom_center_widget.place(relx=0.5, rely=0.3, anchor=CENTER)



# Background and icon images
img = PhotoImage(file='../WaveForm/gui/pics/Logo.png')
logo_top = PhotoImage(file='../WaveForm/gui/pics/TopLogo.png')
play_button = PhotoImage(file='../WaveForm/gui/buttons/play_button.png')
pause_button = PhotoImage(file='../WaveForm/gui/buttons/pause_button.png')
next_button = PhotoImage(file='../WaveForm/gui/buttons/next_button.png')
previous_button = PhotoImage(file='../WaveForm/gui/buttons/previous_button.png')
root.iconphoto(False, img)


# Grid settings
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=3)
main_frame.grid_columnconfigure(2, weight=1)

main_frame.grid_rowconfigure(0, weight=0)
main_frame.grid_rowconfigure(1, weight=4)
main_frame.grid_rowconfigure(2, weight=0)

logo_label = Label(top_frame, image=logo_top, bg='#1E052A')
logo_label.grid(row=0, column=1, sticky='e', padx=10, pady=5)
Label(top_frame, bg='#1E052A').grid(row=0, column=0, sticky='w')
top_frame.grid_columnconfigure(0, weight=1)

# Playlist page grid
left_frame.grid_rowconfigure(0,  weight=1)
left_frame.grid_rowconfigure(1,  weight=10)
left_frame.grid_columnconfigure(0, weight=1)

search_frame.grid_rowconfigure(0, weight=1)
#search_frame.grid_rowconfigure(1, weight=1)
search_frame.grid_columnconfigure(0, weight=1)

# Playlist page grid
middle_frame.grid_rowconfigure(0,  weight=1)
middle_frame.grid_rowconfigure(1,  weight=2)
middle_frame.grid_columnconfigure(0, weight=1)

#middle_frame.grid_rowconfigure(3,  weight=1)

# Right Frame Grid

right_frame.grid_rowconfigure(0, weight=2)
right_frame.grid_rowconfigure(1, weight=3)
right_frame.grid_columnconfigure(0, weight=1)

# Bottom frame grid
bottom_frame_mid.grid_rowconfigure(0, weight=1)
bottom_frame_mid.grid_rowconfigure(1, weight=1)
bottom_frame_mid.grid_columnconfigure(0, weight=1)
bottom_frame_mid.grid_columnconfigure(1, weight=1)
bottom_frame_mid.grid_columnconfigure(2, weight=1)

# Window and label width

# Labels

# Left frame labels

# Search 

Label(search_type_frame, text="Search", font=("Arial", 14), fg='white', bg='#3A0C60')
search_entry = Entry(search_type_frame, font=("Arial", 12), width=30)
search_entry.pack(side=LEFT, padx=5, pady=5, fill="x", expand=True)
Label(search_buttons_frame, text="Buttons_to_search", font=("Arial", 14), fg='white', bg='#3A0C60').pack(pady=5)
# Pinned playlists
Label(pinned_playlist_frame, text="Playlists", font=("Arial", 14), fg='white', bg='#3A0C60').pack(pady=5)
playlist1 = Button(pinned_playlist_frame, text="Liked songs", width=20, height=2, fg='black', bg='red')
playlist1.pack(pady=5)
playlist2 = Button(pinned_playlist_frame, text="UK Dubstep", width=20, height=2, fg='black', bg='black')
playlist2.pack(pady=5)

# Middle frame labels
Label(header_frame, text='Playlist: UK Bassline', font=("Arial", 24, "bold"), fg='white', bg='#3A0C60').pack(pady=1)
canvas = Canvas(songlist_frame, highlightthickness=0)
canvas.pack(fill="both", expand=True, pady=5)


start_color = (133, 14, 185)  # Color start (purple)
end_color = (60, 6, 83)      # Color end (darker purple)

playlist_right_frame_label = Label(now_playing_frame, text='UK Bassline', font=("Arial", 18, "bold"), fg='white', bg='#3A0C60')
playlist_right_frame_label.pack(side=TOP, padx=0, pady=0)
album_art_label = Label(now_playing_frame, bg='yellow')

album_art_label.pack(side=TOP, padx=0, pady=0)
#title_label2 = Label(now_playing_frame, text="Now Playing", font=("Arial", 18, "bold"), fg='white', bg='#3A0C60').pack(pady=5)
title2_label = Label(now_playing_frame, fg="white",  bg='#3A0C60', font=("Arial", 18, "bold"))
title2_label.pack(side=TOP, padx=0, pady=0)
#title2_label.bind("<Button-1>", now_playing)

artist2_label = Label(now_playing_frame, fg="white",  bg='#3A0C60', font=("Arial", 14, "bold"))
artist2_label.pack(side=TOP, padx=0, pady=2)
#artist2_label.bind("<Button-1>", now_playing)

def display_album_art(song_name):
    filepath = os.path.join('app/data/Music', song_name)
    if filepath.endswith('.mp3'):
        try:
            audio = MP3(filepath, ID3=ID3)
            album_art_found = False 
            for tag in audio.tags.values():
                if isinstance(tag, APIC):  
                    album_art = Image.open(io.BytesIO(tag.data))
                    album_art = album_art.resize((100, 100))  
                    album_art = ImageTk.PhotoImage(album_art)
                    album_art_label.image = album_art  
                    album_art_label.config(image=album_art)
                    album_art_found = True
                    break
            if not album_art_found:
                album_art_label.config(image='')
                album_art_label.image = None
        except Exception as e:
            print("Couldn't find song cover", e)
            album_art_label.config(image='')  
            album_art_label.image = None
    else:
        album_art_label.config(image='')  
        album_art_label.image = None

# def create_vertical_gradient(canvas, color1, color2):
#     canvas_width = canvas.winfo_width()  # Get canvas width dynamically
#     canvas_height = canvas.winfo_height()  # Get canvas height dynamically
#     for i in range(canvas_height):
#         ratio = i / canvas_height  # Calculate the color ratio based on the current position
#         r = int(color1[0] + (color2[0] - color1[0]) * ratio)
#         g = int(color1[1] + (color2[1] - color1[1]) * ratio)
#         b = int(color1[2] + (color2[2] - color1[2]) * ratio)
#         color = f'#{r:02x}{g:02x}{b:02x}'  # Convert RGB to hex color
#         canvas.create_rectangle(0, i, canvas_width, i + 1, fill=color, outline='')

# def update_canvas_gradient(event=None):
#     canvas.delete("all")  # Clear the canvas before redrawing
#     create_vertical_gradient(canvas, start_color, end_color)  # Redraw the gradient

# # Ensure the gradient updates when the window is resized
# songlist_frame.bind("<Configure>", update_canvas_gradient)

# # Initial gradient setup on start
# update_canvas_gradient()

song_listbox = Listbox(songlist_frame, bg='#3C0F64', fg='white', relief="flat")
song_listbox.place(relwidth=1, relheight=1)

# Now songs are static, in future they will be dynamic
os.chdir('app/data/Music')
songs = os.listdir()
for s in songs:
    song_listbox.insert(END, s)





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
            #display_album_art(currentsong)
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
        title2_label.config(text=f"{title}")
        artist2_label.config(text=f"{artist}")
        
    else:
        currentsong_display = currentsong[:20] + "..." if len(currentsong) > 20 else currentsong
        title_label.config(text=f"{currentsong_display}")
        artist_label.config(text=f"{currentsong_display}")
        title2_label.config(text=f"{currentsong_display}")
        artist2_label.config(text=f"{currentsong_display}")
        
    
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
        bottom_center_bar.after(1000, progress_bar)

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
    
    bottom_center_bar.after(500, lambda: set_user_sliding(False))

    
def set_user_sliding(value):
    global user_sliding
    user_sliding = value

# def create_widgets(self):
#     self.create_bottom_widgets()
    
# def create_bottom_widgets(self):
#     self.create_
    
# Left panel buttons
def create_playlist_button(parent, text, bg_color, icon=None):
    return Button(parent, text=text, font=("Arial", 14, "bold"), width=20, height=2, borderwidth=0, highlightthickness=0,
                  activebackground='#501908', cursor='hand2')
    
    
    
# Bottom left frame labels

title_label = Label(bottom_left_widget, fg="white",  bg='#1E052A', font=("Arial", 18, "bold"))
title_label.pack(side=TOP, padx=0, pady=10)
title_label.bind("<Button-1>", now_playing)

artist_label = Label(bottom_left_widget, fg="white",  bg='#1E052A', font=("Arial", 14, "bold"))
artist_label.pack(side=TOP, padx=7, pady=5)
title_label.bind("<Button-1>", now_playing)

# Bottom center frame labels
previous_label = Label(bottom_center_widget, image=previous_button, bg='#1E052A')
previous_label.pack(side="left", pady=40, padx=5)
previous_label.bind("<Button-1>", previous_song)

play_pause_label = Label(bottom_center_widget, image=play_button, bg='#1E052A')
play_pause_label.pack(side="left", pady=40, padx=15)
play_pause_label.bind("<Button-1>", play_pause_song)

next_label = Label(bottom_center_widget, image=next_button, bg='#1E052A')
next_label.pack(side="left", pady=40, padx=5)
next_label.bind("<Button-1>", next_song)

time_elapsed_label = customtkinter.CTkLabel(bottom_center_bar, text="00:00")
time_elapsed_label.pack(side="left", pady=5, padx=5)

progress_slider = customtkinter.CTkSlider(bottom_center_bar, from_=0, to=100, command=slide_music)
progress_slider.set(0)
progress_slider.pack(side="left", pady=5, padx=5, expand=True, fill="x")

time_remaining_label = customtkinter.CTkLabel(bottom_center_bar, text="-00:00")
time_remaining_label.pack(side="left", pady=5, padx=5)

#Volume bar
volume_label = customtkinter.CTkLabel(bottom_frame_right, text="Volume: 100%")
volume_label.pack(pady=20)

volume_bar = customtkinter.CTkSlider(bottom_frame_right, from_=0, to=100, command=control_volume)

volume_bar.set(100)
volume_bar.pack(pady=10, fill="x")



root.mainloop()
