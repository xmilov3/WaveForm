from tkinter import Menu, Toplevel, Label
from app.func.session import user_session

def bind_logo_click(logo_label, page_manager):
    logo_label.bind("<Button-1>", lambda event: show_user_menu(event, logo_label, page_manager))

def show_user_menu(event, logo_label, page_manager):
    username = user_session.username if user_session.username else "Unknown User"
    menu = Menu(logo_label, tearoff=0, bg="white", fg="black", font=("Arial", 12))
    menu.add_command(label=f"Logged as: {username}", state="disabled")
    menu.add_separator()
    # menu.add_command(label="Settings", command=lambda: open_settings(page_manager))
    menu.add_command(label="Exit", command=quit_app)
    menu.post(event.x_root, event.y_root)

# def open_settings(page_manager):
    # page_manager.show_dynamic_panel("SettingsPanel")

def quit_app():
    exit()
