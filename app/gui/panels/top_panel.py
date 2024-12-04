from tkinter import Frame, Label
from app.func.load_pic_gui import load_top_logo, load_text
from app.func.config import *


def create_top_panel(parent):
    top_frame = Frame(parent, bg='#150016')
    top_frame.grid(row=0, column=0, columnspan=3, sticky='ew', padx=1, pady=1)
    
    top_logo_img = load_top_logo(size=(100, 70))
    logo_label = Label(top_frame, image=top_logo_img, bg='#150016')
    logo_label.image = top_logo_img
    logo_label.grid(row=0, column=2, sticky='e', padx=10, pady=5)

    text_logo_img = load_text(size=(350, 80))
    text_logo_label = Label(top_frame, image=text_logo_img, bg="#150016")
    text_logo_label.image = text_logo_img
    text_logo_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)

    return top_frame
