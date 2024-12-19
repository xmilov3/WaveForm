import tkinter as tk
from init_page import InitPage
from login_window import LoginPage



class PageManager:
    def __init__(self, root):
        self.root = root
        self.pages = {}

    def add_page(self, name, frame):
        self.pages[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, name):
        for page in self.pages.values():
            page.grid_remove()
        self.pages[name].grid()
        self.root.update_idletasks()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
