import tkinter as tk
from app.func.config import *


class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg='black')

        label = tk.Label(
            self, 
            text="Welcome to the Main Frame!", 
            font=("Arial", 24, "bold"), 
            fg="white", 
            bg="black"
        )
        label.pack(expand=True, padx=10, pady=10)

