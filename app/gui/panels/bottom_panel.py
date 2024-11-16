from tkinter import Frame, Button, Label, Scale, HORIZONTAL, ACTIVE
from app.func.load_pic_gui import load_button_image
from app.func.music_controller import play_pause_song, next_song, previous_song, progress_bar, slide_music
from app.func.config import *

def create_bottom_panel(parent, song_listbox):
    global currentsong, is_playing

    
    bottom_frame = Frame(parent, bg='#1E052A')
    bottom_frame.grid(row=2, column=0, columnspan=3, sticky='nsew', pady=1)

    bottom_frame_left = Frame(bottom_frame, bg='#1E052A')
    bottom_frame_left.grid(row=0, column=0, sticky='nsew', padx=5)
    #Label(bottom_frame_left, text="Left Panel", font=("Arial", 12), fg='white', bg='#1E052A').pack(pady=5)

    bottom_frame_mid = Frame(bottom_frame, bg='#1E052A')
    bottom_frame_mid.grid(row=0, column=1, sticky='nsew', padx=5)

    prev_button_img = load_button_image("previous")
    play_button_img = load_button_image("play")
    #pause_button_img = load_button_image("pause")
    next_button_img = load_button_image("next")

    previous_button = Button(
        bottom_frame_mid, 
        image=prev_button_img, 
        bg='#1E052A', 
        activebackground='#1E052A',
        borderwidth=0,
        command=lambda: previous_song(
            song_listbox, 
            #is_playing, 
            #song_length, 
            #current_song_position, 
            #song_start_time
            #play_pause_button
            )
        )
    previous_button.image = prev_button_img
    previous_button.grid(row=0, column=0, padx=5)


    play_pause_button = Button(
        bottom_frame_mid, 
        image=play_button_img,
        bg='#1E052A', 
        activebackground='#1E052A',
        borderwidth=0,
        command=lambda: update_play_pause(
        song_listbox.get(ACTIVE),
        song_listbox,
        play_pause_button
        )
    )
    play_pause_button.image = play_button_img
    play_pause_button.grid(row=0, column=1, padx=5)

    next_button = Button(
        bottom_frame_mid, 
        image=next_button_img, 
        bg='#1E052A', 
        activebackground='#1E052A',
        borderwidth=0,
        command=lambda: next_song(song_listbox, 
                                  is_playing, 
                                  song_length, 
                                  current_song_position, 
                                  song_start_time
                                  )
        )
    next_button.image = next_button_img
    next_button.grid(row=0, column=2, padx=5)

    bottom_frame_right = Frame(bottom_frame, bg='#1E052A')
    bottom_frame_right.grid(row=0, column=2, sticky='nsew', padx=5)

    Label(bottom_frame_right, text="Right Panel", font=("Arial", 12), fg='white', bg='#1E052A').pack(pady=5)

    bottom_center_bar = Frame(bottom_frame_mid, bg='#1E052A')
    bottom_center_bar.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=10)

    time_elapsed_label = Label(bottom_center_bar, text="00:00", font=("Arial", 12), fg='white', bg='#1E052A')
    time_elapsed_label.grid(row=0, column=0, padx=5)

    progress_slider = Scale(bottom_center_bar, from_=0, to=100, orient=HORIZONTAL, length=400, bg='#3A0C60',
                            troughcolor='#501908', sliderrelief="flat", highlightthickness=0,
                            command=lambda value: slide_music(value, time_elapsed_label, time_elapsed_label, bottom_center_bar))
    progress_slider.grid(row=0, column=1, padx=10)

    time_remaining_label = Label(bottom_center_bar, text="00:00", font=("Arial", 12), fg='white', bg='#1E052A')
    time_remaining_label.grid(row=0, column=2, padx=5)

    progress_bar(time_remaining_label, time_elapsed_label, progress_slider, bottom_center_bar)

    return bottom_frame

def update_play_pause(currentsong, song_listbox, play_pause_button):
    global is_playing, song_length, current_song_position, song_start_time
    is_playing, song_length, current_song_position, song_start_time = play_pause_song(
        currentsong,
        is_playing,
        song_listbox,
        play_pause_button,
        song_length,
        current_song_position,
        song_start_time
    )
