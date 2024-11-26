from tkinter import Label, Button, PhotoImage, FLAT
from app.func.load_pic_gui import load_play_button, load_pause_button, load_previous_button, load_next_button
from app.func.config import *

def create_play_pause_button(parent, play_command, pause_command):
    play_button_img = load_play_button()
    pause_button_img = load_pause_button()

    button = Label(parent, image=play_button_img, bg='#1E052A', borderwidth=0, highlightthickness=0)
    button.image_play = play_button_img 
    button.image_pause = pause_button_img  
    button.is_playing = False  

    def toggle_image(event=None):
        print(f"Before toggle: is_playing={button.is_playing}")  
        if button.is_playing:
            button.config(image=button.image_play)  
            pause_command()  
        else:
            button.config(image=button.image_pause)  
            play_command() 
        button.is_playing = not button.is_playing  
        print(f"After toggle: is_playing={button.is_playing}")  

    button.bind("<Button-1>", toggle_image)  

    return button


def create_previous_button(parent, command):
    previous_button_img = load_previous_button()
    button = Label(parent, image=previous_button_img, bg='#1E052A')
    button.image = previous_button_img 
    button.bind("<Button-1>", command)
    return button


def create_next_button(parent, command):
    next_button_img = load_next_button()
    button = Label(parent, image=next_button_img, bg='#1E052A')
    button.image = next_button_img  
    button.bind("<Button-1>", command)
    return button
