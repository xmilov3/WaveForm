from tkinter import *
import os

def load_logo():
    img = PhotoImage(file='app/gui/assets/pics/Logo.png')
    return img

def load_top_logo():
    logo_top = PhotoImage(file='app/gui/assets/pics/TopLogo.png')
    return logo_top



def load_button_image(button_type):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    assets_dir = os.path.join(base_dir, "../gui/assets/buttons")
    
    button_images = {
        "play": os.path.join(assets_dir, "play_button.png"),
        "pause": os.path.join(assets_dir, "pause_button.png"),
        "next": os.path.join(assets_dir, "next_button.png"),
        "previous": os.path.join(assets_dir, "previous_button.png"),
    }
    
    image_path = button_images.get(button_type, "")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    return PhotoImage(file=image_path)
