from tkinter import *

def load_logo():
    img = PhotoImage(file='app/gui/assets/pics/Logo.png')
    return img

def load_top_logo():
    logo_top = PhotoImage(file='app/gui/assets/pics/TopLogo.png')
    return logo_top


def load_button_image(button_type):
    button_images = {
        "play": "app/gui/assets/buttons/play_button.png",
        "pause": "app/gui/assets/buttons/pause_button.png",
        "next": "app/gui/assets/buttons/next_button.png",
        "previous": "app/gui/assets/buttons/previous_button.png",
    }
    return PhotoImage(file=button_images.get(button_type, ""))

