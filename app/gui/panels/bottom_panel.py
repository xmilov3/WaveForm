from tkinter import Frame, Label
from tkinter import *



def create_bottom_panel(main_frame):
    bottom_frame = Frame(main_frame, bg='#1E052A')
    bottom_frame.grid(row=2, column=0, columnspan=3, sticky='nsew', pady=1)
    
    bottom_left_widget = Label(bottom_frame, bg='#1E052A')
    bottom_left_widget.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)

    bottom_center_widget = Label(bottom_frame, bg='#1E052A')
    bottom_center_widget.grid(row=1, column=1, sticky='nsew', padx=50)
    bottom_center_widget.place(relx=0.5, rely=0.4, anchor=CENTER)

    bottom_center_bar = Label(bottom_frame, bg='#1E052A')
    bottom_center_bar.grid(row=2, column=1, sticky='nsew', padx=50)

    bottom_right_widget = Label(bottom_frame, bg='#1E052A')
    bottom_right_widget.grid(row=0, column=2, sticky='nsew', padx=1, pady=1)
    
    return bottom_frame