from tkinter import Frame, Label


class SettingsPanel(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#150016")
        Label(self, text="Settings Panel", font=("Arial", 24), fg="white", bg="#150016").pack(pady=50)
