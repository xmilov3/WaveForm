from tkinter import Frame, Label
from app.func.config import *


def create_main_frame(root):
    main_frame = Frame(root, bg='black')
    main_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
    return main_frame