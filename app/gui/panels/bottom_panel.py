from tkinter import Frame, Label, Scale, HORIZONTAL, ACTIVE
from app.gui.widgets import create_play_pause_button, create_previous_button, create_next_button
from app.func.music_controller import play_pause_song, next_song, previous_song, progress_bar, slide_music, stop_song, set_user_sliding
from app.func.config import *

def create_bottom_panel(parent, song_listbox):
    global currentsong, is_playing
    is_playing = False  

    bottom_frame = Frame(parent, bg='#1E052A')
    bottom_frame.grid(row=2, column=0, columnspan=3, sticky='nsew', pady=1)

    bottom_frame_left = Frame(bottom_frame, bg='#1E052A')
    bottom_frame_left.grid(row=0, column=0, sticky='nsew', padx=5)

    bottom_frame_mid = Frame(bottom_frame, bg='#1E052A')
    bottom_frame_mid.grid(row=0, column=1, sticky='nsew', padx=5)

    bottom_frame_right = Frame(bottom_frame, bg='#1E052A')
    bottom_frame_right.grid(row=0, column=2, sticky='nsew', padx=5)

    try:
        play_button_img = create_play_pause_button.__globals__['load_play_button']()
        pause_button_img = create_play_pause_button.__globals__['load_pause_button']()
    except Exception as e:
        print(f"Error while loading buttons: {e}")
        return bottom_frame

    def previous_command():
        previous_song(song_listbox, play_pause_button, play_button_img, pause_button_img)

    def play_pause_command():
        global is_playing
        currentsong = song_listbox.get(ACTIVE)
        if not currentsong:
            print("No song selected!")
            return

        is_playing = play_pause_song(
            currentsong, is_playing, play_pause_button, play_button_img, pause_button_img
        )

    def next_command():
        next_song(song_listbox, play_pause_button, play_button_img, pause_button_img)

    previous_button = create_previous_button(bottom_frame_mid, lambda e=None: previous_command())
    play_pause_button = create_play_pause_button(
        bottom_frame_mid,
        play_command=play_pause_command,  
        pause_command=play_pause_command  
    )
    next_button = create_next_button(bottom_frame_mid, lambda e=None: next_command())

    previous_button.grid(row=0, column=0, padx=5)
    play_pause_button.grid(row=0, column=1, padx=5)
    next_button.grid(row=0, column=2, padx=5)

    bottom_center_bar = Frame(bottom_frame_mid, bg='#1E052A')
    bottom_center_bar.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=10)

    time_elapsed_label = Label(bottom_center_bar, text="00:00", font=("Arial", 12), fg='white', bg='#1E052A')
    time_elapsed_label.grid(row=0, column=0, padx=5)

    progress_slider = Scale(
        bottom_center_bar,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        length=400,
        bg='#3A0C60',
        troughcolor='#501908',
        sliderrelief="flat",
        highlightthickness=0,
        command=lambda value: None
    )

    progress_slider.bind(
    "<ButtonPress-1>",
    lambda e: set_user_sliding(True)  
    )
    progress_slider.bind(
        "<ButtonRelease-1>",
        lambda e: slide_music(
            progress_slider.get(),
            time_elapsed_label,
            time_remaining_label,
            bottom_frame
        ) 
    )



    progress_slider.grid(row=0, column=1, padx=10)


    time_remaining_label = Label(bottom_center_bar, text="-00:00", font=("Arial", 12), fg='white', bg='#1E052A')
    time_remaining_label.grid(row=0, column=2, padx=5)

    progress_bar(time_remaining_label, time_elapsed_label, progress_slider, bottom_center_bar)

    return bottom_frame



def update_play_pause(currentsong, song_listbox, play_button, play_button_img, pause_button_img):
    global is_playing
    if not currentsong:
        currentsong = song_listbox.get(ACTIVE)
        if not currentsong:
            print("No song selected!")
            return

    is_playing = play_pause_song(
        currentsong,
        is_playing,
        play_button,
        play_button_img,
        pause_button_img
    )
