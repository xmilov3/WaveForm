import tkinter as tk


class PageManager:
    def __init__(self, root):
        self.root = root
        self.pages = {}
        self.dynamic_panels = {}
        self.current_dynamic_panel = None

    def add_page(self, name, frame, is_dynamic=False):
        if is_dynamic:
            self.dynamic_panels[name] = frame
        else:
            self.pages[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, name, *args):
        for page in self.pages.values():
            page.grid_remove()

        if name in self.pages:
            self.pages[name].grid()

        elif name in self.dynamic_panels:
            if self.current_dynamic_panel:
                self.current_dynamic_panel.grid_remove()
            dynamic_page = self.dynamic_panels[name](*args)
            dynamic_page.grid(row=0, column=0, sticky="nsew")
            self.current_dynamic_panel = dynamic_page

        self.root.update_idletasks()

    def add_dynamic_panel(self, name, frame_creator):
        self.dynamic_panels[name] = frame_creator


    def show_dynamic_panel(self, dynamic_panel_name, playlist_name):
        if self.current_dynamic_panel:
            self.current_dynamic_panel.grid_remove()

        create_panel_func = self.dynamic_panels[dynamic_panel_name]

        middle_frame = create_panel_func(self.root, playlist_name)
        middle_frame.grid(row=1, column=1, sticky="nsew")

        self.current_dynamic_panel = middle_frame


    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
