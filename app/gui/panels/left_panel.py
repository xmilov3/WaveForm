from tkinter import *
from tkinter import ttk, Menu
from tkinter import simpledialog, filedialog, messagebox
from app.func.add_song import add_song
from app.db.db_operations import insert_song
from app.func.add_playlist import create_empty_playlist, import_playlist_from_folder
from app.func.playlist_utils import update_playlist_buttons, show_context_menu, change_playlist_cover, delete_playlist, fetch_playlists
from app.func.playlist_utils import *





def create_left_panel(parent, page_manager):
    left_frame = Frame(parent, bg='#1E052A', borderwidth=0)
    left_frame.grid(row=1, column=0, sticky='nsew')

    buttons_frame = Frame(left_frame, bg='#2d0232')
    buttons_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    playlist_frame = Frame(left_frame, bg='#2d0232')
    playlist_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

    left_frame.playlist_frame = playlist_frame

    style = ttk.Style()
    style.configure(
        "Custom.TButton",
        font=("Arial", 14, "bold"),
        foreground='#FFFFFF',
        background='#50184A',
        padding=5
    )
    style.map(
        "Custom.TButton",
        background=[('active', '#845162')],
        foreground=[('active', '#FFFFFF')]
    )

    ttk.Button(
        buttons_frame,
        text="Add Song",
        style="Custom.TButton",
        command=lambda: add_song_with_playlist(page_manager)
    ).pack(fill="x", padx=10, pady=5)

    ttk.Button(
        buttons_frame,
        text="Create Playlist",
        style="Custom.TButton",
        command=lambda: create_empty_playlist(playlist_frame, page_manager)
    ).pack(fill="x", padx=10, pady=5)

    ttk.Button(
        buttons_frame,
        text="Import Playlist",
        style="Custom.TButton",
        command=lambda: import_playlist_from_folder(playlist_frame, page_manager)
    ).pack(fill="x", padx=10, pady=5)

    ttk.Button(
        buttons_frame,
        text="Analyze Song",
        style="Custom.TButton",
        command=lambda: add_song_with_playlist(page_manager)
    ).pack(fill="x", padx=10, pady=5)

    update_playlist_buttons(playlist_frame, delete_playlist, change_playlist_cover, page_manager)

    return left_frame



def populate_playlists(playlist_frame, page_manager):
    for widget in playlist_frame.winfo_children():
        widget.destroy()

    playlists = fetch_playlists()

    if playlists:
        for i, playlist_name in enumerate(playlists):
            playlist_button = Button(
                playlist_frame,
                text=playlist_name,
                font=("Arial", 14, "bold"),
                fg='black',
                bg='#50184A',
                # activebackground='#845162',
                # activeforegrouknd='black',
                borderwidth=0,
                command=lambda name=playlist_name: page_manager.show_dynamic_panel("MiddlePanel", name)
            )
            playlist_button.grid(row=i, column=0, sticky="ew", padx=5, pady=5)

            playlist_button.configure(
                fg='black',
                bg='#50184A',
                # activebackground='#845162',
                # activeforeground='black'
            )
    else:
        Label(
            playlist_frame,
            text="No playlists available.",
            font=("Arial", 14, "bold"),
            fg="gray",
            bg="#2d0232"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    playlist_frame.grid_columnconfigure(0, weight=1)





def handle_playlist_selection(event, page_manager, listbox):
    selected_index = listbox.curselection()
    if selected_index:
        playlist_name = listbox.get(selected_index)
        page_manager.show_dynamic_panel("MiddlePanel", playlist_name)


def update_playlist_buttons(playlist_frame, delete_playlist_callback, change_cover_callback, page_manager):
    for widget in playlist_frame.winfo_children():
        widget.destroy()

    playlists = fetch_playlists()

    for i, playlist_name in enumerate(playlists):
        button = ttk.Button(
            playlist_frame,
            text=playlist_name,
            style="Custom.TButton",
            command=lambda name=playlist_name: page_manager.show_dynamic_panel("MiddlePanel", name)
        )
        button.grid(row=i, column=0, sticky="ew", padx=5, pady=5)

        button.bind("<Button-3>", lambda event, name=playlist_name: show_context_menu(event, name, playlist_frame, page_manager))

    playlist_frame.grid_columnconfigure(0, weight=1)


def show_context_menu(event, playlist_name, playlist_frame, page_manager):
    menu = Menu(None, tearoff=0)
    menu.add_command(
        label="Delete Playlist",
        command=lambda: delete_playlist_wrapper(playlist_name, playlist_frame, page_manager)
    )
    menu.add_command(
        label="Change Cover",
        command=lambda: change_playlist_cover(playlist_name)
    )
    menu.post(event.widget.winfo_rootx() + event.x, event.widget.winfo_rooty() + event.y)


def delete_playlist_wrapper(playlist_name, playlist_frame, page_manager):
    response = messagebox.askyesno("Delete Playlist", f"Are you sure you want to delete '{playlist_name}'?")
    if response:
        delete_playlist(playlist_name, playlist_frame, update_playlist_buttons, page_manager)


def add_song_with_playlist(page_manager):
    playlists = fetch_playlists()
    if not playlists:
        messagebox.showwarning("Warning", "No playlists available. Add a playlist first.")
        return

    selected_playlist = simpledialog.askstring("Select Playlist", f"Choose playlist:\n{', '.join(playlists)}")
    if selected_playlist:
        file_path = filedialog.askopenfilename(
            title="Select a music file",
            filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")]
        )
        if file_path:
            add_song(file_path, selected_playlist)
            messagebox.showinfo("Success", f"Song added to playlist '{selected_playlist}'.")
        else:
            messagebox.showinfo("Info", "No file selected.")

