from tkinter import Frame, Label
from app.func.load_pic_gui import load_top_logo
from app.func.config import *


def create_top_panel(main_frame):
    top_frame = Frame(main_frame, bg='#1E052A')
    top_frame.grid(row=0, column=0, columnspan=3, sticky='ew', padx=1, pady=1)
    logo_label = Label(top_frame, image=load_top_logo(), bg='#1E052A')
    logo_label.grid(row=0, column=1, sticky='e', padx=10, pady=5)
    Label(top_frame, bg='#1E052A').grid(row=0, column=0, sticky='w')
    return top_frame
