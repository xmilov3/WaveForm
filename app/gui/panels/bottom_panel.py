from tkinter import Frame, Label
from tkinter import *
from app.func.config import *



def create_bottom_panel(main_frame):
    bottom_frame_left = Frame(main_frame, bg='#1E052A')
    bottom_frame_left.grid(row=2, column=0, sticky='nsew', pady=1)
    bottom_frame_mid = Frame(main_frame, bg='#1E052A')
    bottom_frame_mid.grid(row=2, column=1, sticky='nsew', pady=1)
    bottom_frame_right = Frame(main_frame, bg='#1E052A')
    bottom_frame_right.grid(row=2, column=2, sticky='ew', pady=1)
    # Widgets
    bottom_left_widget = Label(bottom_frame_left, bg='#1E052A')
    bottom_left_widget.grid(row=0, column=0, sticky='nsew')
    bottom_left_widget.pack(pady=1)
    # Bottom center widget
    bottom_center_widget = Label(bottom_frame_mid, bg='#1E052A')
    bottom_center_widget.grid(row=1, column=1, sticky='nsew', padx=50)
    bottom_center_widget.place(relx=0.5, rely=0.4, anchor=CENTER)
    bottom_center_bar = Label(bottom_frame_mid, bg='#1E052A')
    bottom_center_bar.grid(row=2, column=1, sticky='nsew')
    return bottom_frame_left