from tkinter import messagebox, Menu, Frame, Button, filedialog, RIGHT, ttk
from app.db.database import create_connection
from app.func.utils import fetch_playlists

def update_playlist_buttons(playlist_frame, delete_playlist_callback, change_cover_callback, page_manager):
    for widget in playlist_frame.winfo_children():
        widget.destroy()

    playlists = fetch_playlists()

    for i, playlist_name in enumerate(playlists):
        playlist_button = Button(
            playlist_frame,
            text=playlist_name,
            font=("Arial", 14, "bold"),
            fg="#FFFFFF",
            bg="#50184A",
            activebackground="#50184A",
            activeforeground="#FFFFFF"
        )
        playlist_button.grid(row=i, column=0, sticky="ew", padx=0, pady=1)
        playlist_button.bind("<Button-3>", lambda event, name=playlist_name: show_playlist_menu(
            event, name, playlist_frame, delete_playlist_callback, change_cover_callback
        ))
        playlist_button.bind("<Button-1>", lambda event, name=playlist_name: page_manager.show_dynamic_panel("MiddlePanel", name))
    playlist_frame.columnconfigure(0, weight=1)



def delete_playlist(playlist_name, playlist_frame, update_playlist_buttons, page_manager):
    try:
        connection = create_connection()
        if not connection:
            messagebox.showerror("Error", "Failed to connect to the database.")
            return
        
        cursor = connection.cursor()
        query = "DELETE FROM playlists WHERE name = %s"
        cursor.execute(query, (playlist_name,))
        connection.commit()
        
        messagebox.showinfo("Success", f"Playlist '{playlist_name}' deleted successfully!")
        update_playlist_buttons(playlist_frame, delete_playlist, change_playlist_cover, page_manager)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete playlist: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def change_playlist_cover(playlist_name):
    cover_path = filedialog.askopenfilename(
        title="Select New Playlist Cover",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")]
    )
    if not cover_path:
        messagebox.showinfo("Info", "No cover image selected.")
        return

    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = "UPDATE playlists SET playlist_cover_path = %s WHERE name = %s"
        cursor.execute(query, (cover_path, playlist_name))
        connection.commit()

        messagebox.showinfo("Success", f"Cover updated for playlist '{playlist_name}'!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update cover: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


def show_playlist_menu(event, playlist_name, playlist_frame, delete_playlist_callback, change_cover_callback):
    menu = Menu(None, tearoff=0)
    menu.add_command(
        label="Delete Playlist",
        command=lambda: delete_playlist_callback(playlist_name, playlist_frame, update_playlist_buttons)
    )
    menu.add_command(
        label="Change Cover",
        command=lambda: change_cover_callback(playlist_name)
    )
    menu.post(event.widget.winfo_rootx() + event.x, event.widget.winfo_rooty() + event.y)


def initialize_middle_frame(page_manager):
    playlists = fetch_playlists()
    if playlists:
        first_playlist = playlists[0]
        page_manager.show_dynamic_panel("MiddlePanel", first_playlist)
