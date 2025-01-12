import tkinter as tk
from app.func.load_pic_gui import *

class InitPage(tk.Frame):
    def __init__(self, parent, page_manager):
        super().__init__(parent)
        self.page_manager = page_manager
        self.configure(bg="#1E052A")

        init_logo = load_init_logo()
        logo_label = tk.Label(self, image=init_logo, bg="#1E052A")
        logo_label.image = init_logo
        logo_label.pack()

        tk.Label(
            self,
            text="Welcome to WaveForm",
            font=("Arial", 40, "bold"),
            fg="gray",
            bg="#1E052A"
        ).pack(pady=50)

        tk.Button(
            self,
            text="Sign up",
            font=("Arial", 18, "bold"),
            bg="#9C27B0",
            fg="black",
            width=20,
            height=2,
            command=lambda: self.page_manager.show_page("RegisterPage")
        ).pack(pady=20)

        tk.Label(
            self,
            text="Or",
            font=("Arial", 18),
            fg="gray",
            bg="#1E052A"
        ).pack(pady=10)

        tk.Button(
            self,
            text="Sign in",
            font=("Arial", 18, "bold"),
            bg="#3C0F64",
            fg="black",
            width=20,
            height=2,
            command=lambda: self.page_manager.show_page("LoginPage")
        ).pack(pady=20)
