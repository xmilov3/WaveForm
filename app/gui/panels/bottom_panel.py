from tkinter import Frame, Label, Scale, HORIZONTAL, ACTIVE, TOP
from app.widgets import create_play_pause_button, create_previous_button, create_next_button
from app.func.config import *
from app.func.music_controller import (
    play_pause_song, next_song, previous_song, progress_bar, slide_music, 
    stop_song, set_user_sliding, initialize_first_song, control_volume, 
    update_next_in_queue, initialize_song_listbox, current_song_listbox, set_current_song_by_index, play_selected_song, update_now_playing
)

def create_bottom_panel(
    main_frame, 
    song_listbox, 
    queue_text_label, 
    playlist_name,
    playlist_label, 
    album_art_label, 
    title_label, 
    artist_label,
    update_next_queue, 
    update_now_playing
):
    
    
    global is_playing, user_sliding, current_song_position, song_length, currentsong, song_start_time

    

    is_playing = False
    user_sliding = False
    current_song_position = 0
    song_length = 0
    currentsong = None
    song_start_time = 0

    bottom_frame = Frame(main_frame, bg='#150016')
    bottom_frame.grid(row=2, column=0, columnspan=3, sticky='nsew', pady=1)

    def update_song_listbox(new_song_listbox):
        nonlocal song_listbox
        song_listbox = new_song_listbox
        print("Song listbox updated in bottom_panel")

    bottom_frame.update_song_listbox = update_song_listbox



    bottom_frame_left = Frame(bottom_frame, bg='#150016')
    bottom_frame_left.grid(row=0, column=0, sticky='w', padx=10)

    title_label = Label(
        bottom_frame_left,
        title_label,
        fg="gray",
        bg='#150016',
        font=("Arial", 18, "bold"),
        anchor="w",
        width=30
    )
    title_label.pack(side=TOP, anchor="w", padx=5, pady=2)

    artist_label = Label(
        bottom_frame_left,
        artist_label,
        fg="gray",
        bg='#150016',
        font=("Arial", 14),
        anchor="w",
        width=30
    )
    artist_label.pack(side=TOP, anchor="w", padx=5, pady=2)

    bottom_frame_mid = Frame(bottom_frame, bg='#150016')
    bottom_frame_mid.grid(row=0, column=1, sticky='nsew')

    try:
        play_button_img = create_play_pause_button.__globals__['load_play_button']()
        pause_button_img = create_play_pause_button.__globals__['load_pause_button']()
    except Exception as e:
        print(f"Error while loading buttons: {e}")

    
    

    def play_pause_command():
        global is_playing, currentsong
        if not song_listbox or song_listbox.size() == 0:
            print("No songs in the playlist!")
            return

        if currentsong is None:
            selected_index = song_listbox.curselection()
            if not selected_index:
                print("No song selected! Setting first song as default.")
                currentsong = set_current_song_by_index(song_listbox, 0)
            else:
                currentsong = set_current_song_by_index(song_listbox, selected_index[0])

        if currentsong:
            print(f"Toggling play/pause for: {currentsong}")
            is_playing = play_pause_song(
                currentsong,
                is_playing,
                play_pause_button,
                play_button_img,
                pause_button_img,
                title_label,
                artist_label
            )
            update_now_playing(playlist_label, album_art_label, title_label, artist_label, playlist_name)


    def next_command():
        global is_playing, currentsong

        selected_index = song_listbox.curselection()
        if not selected_index:
            print("No song selected in next_command! Setting to first song.")
            currentsong = set_current_song_by_index(song_listbox, 0)
            return

        next_index = (selected_index[0] + 1) % song_listbox.size()
        currentsong = set_current_song_by_index(song_listbox, next_index)

        if currentsong:
            is_playing = True
            print(f"Playing next song: {currentsong}")
            play_selected_song(
                currentsong,
                title_label,
                artist_label,
                album_art_label,
                time_elapsed_label,
                time_remaining_label,
                progress_slider
            )


    def previous_command():
        global is_playing, current_song_position, currentsong
        previous_song(
            currentsong,
            play_pause_button,
            play_button_img,
            pause_button_img,
            title_label,
            artist_label,
            time_elapsed_label,
            time_remaining_label,
            progress_slider,
            queue_text_label,
            playlist_name,
            playlist_label,
            album_art_label,
            bottom_frame_left
        )
        is_playing = True
        current_song_position = 0

        update_now_playing(playlist_label, album_art_label, title_label, artist_label, playlist_name)

    previous_button = create_previous_button(bottom_frame_mid, lambda e=None: previous_command())
    play_pause_button = create_play_pause_button(
        bottom_frame_mid,
        play_command=lambda: play_pause_command(),
        pause_command=lambda: play_pause_command()
    )
    next_button = create_next_button(bottom_frame_mid, lambda e=None: next_command())



    previous_button.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    play_pause_button.grid(row=0, column=1, padx=10, pady=5)
    next_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    # Progress Bar
    bottom_center_bar = Frame(bottom_frame_mid, bg='#150016')
    bottom_center_bar.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=10)

    time_elapsed_label = Label(
        bottom_center_bar,
        text="00:00",
        font=("Arial", 12),
        fg='gray',
        bg='#150016',
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
        bg='#845162',
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
        currentsong
    ))
    progress_slider.grid(row=0, column=1, padx=10)

    time_remaining_label = Label(
        bottom_center_bar,
        text="-00:00",
        font=("Arial", 12),
        fg='gray',
        bg='#150016',
        anchor="w",
        width=5
    )
    time_remaining_label.grid(row=0, column=2, padx=5)

    bottom_frame_right = Frame(bottom_frame, bg='#150016')
    bottom_frame_right.grid(row=0, column=2, sticky='nsew', padx=10)

    volume_label = Label(
        bottom_frame_right,
        text="Volume: 100%",
        font=("Arial", 12),
        fg='gray',
        bg='#150016',
        anchor="center"
    )
    volume_label.grid(row=0, column=0, pady=10)

    volume_slider = Scale(
        bottom_frame_right,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        length=200,
        bg='#845162',
        fg='gray',
        troughcolor='#320532',
        sliderrelief="flat",
        sliderlength=15,
        highlightthickness=0,
        borderwidth=0,
        showvalue=False,
        command=lambda value: control_volume(value, volume_label)
    )
    volume_slider.set(50)
    volume_slider.grid(row=1, column=0, padx=10)

    progress_bar(time_remaining_label, time_elapsed_label, progress_slider, bottom_center_bar)

    update_next_queue(queue_text_label, playlist_name)
    update_now_playing(playlist_label, album_art_label, title_label, artist_label, playlist_name)

    return (
        bottom_frame,
        time_remaining_label,
        time_elapsed_label,
        progress_slider,
        play_pause_button,
        play_button_img,
        pause_button_img
    )