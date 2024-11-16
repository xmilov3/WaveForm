from tkinter import Frame, Label
from app.func.load_pic_gui import load_top_logo
from app.func.config import *


def create_top_panel(parent):
    top_frame = Frame(parent, bg='#1E052A')
    top_frame.grid(row=0, column=0, columnspan=3, sticky='ew', padx=1, pady=1)
    
    top_logo_img = load_top_logo()
    
    logo_label = Label(top_frame, image=top_logo_img, bg='#1E052A')
    logo_label.image = top_logo_img
    logo_label.grid(row=0, column=1, sticky='e', padx=10, pady=5)
    Label(top_frame, bg='#1E052A').grid(row=0, column=0, sticky='w')
    return top_frame
