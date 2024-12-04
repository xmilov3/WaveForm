from tkinter import Frame, Label, Scale, HORIZONTAL, ACTIVE, TOP
from app.gui.widgets import create_play_pause_button, create_previous_button, create_next_button
from app.func.music_controller import play_pause_song, next_song, previous_song, progress_bar, slide_music, stop_song, set_user_sliding, initialize_first_song, control_volume
from app.func.config import *
from app.func.music_controller import previous_song



def create_bottom_panel(main_frame, song_listbox):
    global is_playing, user_sliding, current_song_position, song_length, currentsong, song_start_time

    is_playing = False
    user_sliding = False
    current_song_position = 0
    song_length = 0
    currentsong = None
    song_start_time=0

    bottom_frame = Frame(main_frame, bg='#1E052A')
    bottom_frame.grid(row=2, column=0, columnspan=3, sticky='nsew', pady=1)

    bottom_frame_left = Frame(bottom_frame, bg='#1E052A')
    bottom_frame_left.grid(row=0, column=0, sticky='w', padx=10)

    title_label = Label(
        bottom_frame_left,
        fg="gray",
        bg='#1E052A',
        font=("Arial", 18, "bold"),
        anchor="w",
        width=30
    )
    title_label.pack(side=TOP, anchor="w", padx=5, pady=2)

    artist_label = Label(
        bottom_frame_left,
        fg="gray",
        bg='#1E052A',
        font=("Arial", 14),
        anchor="w",
        width=30
    )
    artist_label.pack(side=TOP, anchor="w", padx=5, pady=2)

    bottom_frame_mid = Frame(bottom_frame, bg='#1E052A')
    bottom_frame_mid.grid(row=0, column=1, sticky='nsew')

    try:
        play_button_img = create_play_pause_button.__globals__['load_play_button']()
        pause_button_img = create_play_pause_button.__globals__['load_pause_button']()
    except Exception as e:
        print(f"Error while loading buttons: {e}")
        return bottom_frame

    def play_pause_command():
        global is_playing

        if user_sliding:  
            print("Ignoring Play/Pause toggle during sliding")
            return

        currentsong = song_listbox.get(ACTIVE)
        if not currentsong:
            print("No song selected!")
            return

        is_playing = play_pause_song(
            currentsong,
            is_playing,
            play_pause_button,
            play_button_img,
            pause_button_img,
            title_label,
            artist_label
        )

    def next_command():
        global is_playing, current_song_position

        next_song(
            song_listbox,
            play_pause_button,
            play_button_img,
            pause_button_img,
            title_label,
            artist_label,
            time_elapsed_label,
            time_remaining_label,
            progress_slider
        )

        is_playing = True
        current_song_position = 0


    def previous_command():
        global is_playing, current_song_position

        previous_song(
            song_listbox,
            play_pause_button,
            play_button_img,
            pause_button_img,
            title_label,
            artist_label,
            time_elapsed_label,
            time_remaining_label,
            progress_slider
        )

        is_playing = True
        current_song_position = 0

    previous_button = create_previous_button(bottom_frame_mid, lambda e=None: previous_command())
    play_pause_button = create_play_pause_button(bottom_frame_mid, play_command=lambda: play_pause_command(),
                                                 pause_command=lambda: play_pause_command())
    next_button = create_next_button(bottom_frame_mid, lambda e=None: next_command())

    previous_button.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    play_pause_button.grid(row=0, column=1, padx=10, pady=5)
    next_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    bottom_center_bar = Frame(bottom_frame_mid, bg='#1E052A')
    bottom_center_bar.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=10)

    time_elapsed_label = Label(
        bottom_center_bar,
        text="00:00",
        font=("Arial", 12),
        fg='gray',
        bg='#1E052A',
        anchor="e",
        width=5
    )
    time_elapsed_label.grid(row=0, column=0, padx=5)

    progress_slider = Scale(
        bottom_center_bar,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        length=500,
        bg='#0f000f',
        fg='gray',
        troughcolor='#320532',
        sliderrelief="flat",
        sliderlength=15,
        highlightthickness=0,
        showvalue=False
    )
    progress_slider.configure(borderwidth=0, relief="flat")

    progress_slider.bind("<ButtonPress-1>", lambda e: set_user_sliding(True))
    progress_slider.bind("<ButtonRelease-1>", lambda e: slide_music(
        progress_slider.get(),
        time_elapsed_label,
        time_remaining_label,
        bottom_frame,
        progress_slider,
        play_pause_button,
        play_button_img,
        pause_button_img,
        song_listbox.get(ACTIVE)
    ))


    progress_slider.grid(row=0, column=1, padx=10)

    time_remaining_label = Label(
        bottom_center_bar,
        text="-00:00",
        font=("Arial", 12),
        fg='gray',
        bg='#1E052A',
        anchor="w",
        width=5
    )
    time_remaining_label.grid(row=0, column=2, padx=5)

    bottom_frame_right = Frame(bottom_frame, bg='#1E052A')
    bottom_frame_right.grid(row=0, column=2, sticky='nsew', padx=10)

    volume_label = Label(
        bottom_frame_right,
        text="Volume: 100%",
        font=("Arial", 12),
        fg='gray',
        bg='#1E052A',
        anchor="center"
    )
    volume_label.grid(row=0, column=0, pady=10)

    volume_slider = Scale(
        bottom_frame_right,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        length=200,
        bg='#0f000f',
        fg='gray',
        troughcolor='#320532',
        sliderrelief="flat",
        sliderlength=15,
        highlightthickness=0,
        showvalue=False,
        command=lambda value: control_volume(value, volume_label)
    )
    volume_slider.set(50)
    volume_slider.grid(row=1, column=0, padx=10)

    progress_bar(time_remaining_label, time_elapsed_label, progress_slider, bottom_center_bar)

    return (
        bottom_frame,
        time_remaining_label,
        time_elapsed_label,
        progress_slider,
        title_label,
        artist_label,
        play_pause_button,
        play_button_img,
        pause_button_img,
    )
