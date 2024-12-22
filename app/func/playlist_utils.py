from tkinter import messagebox, Menu, Frame, Button, filedialog, RIGHT, ttk
from app.db.database import create_connection
from app.func.utils import fetch_playlists

def update_playlist_buttons(playlist_frame, delete_playlist_callback, change_cover_callback):
    from app.func.utils import fetch_playlists

    for widget in playlist_frame.winfo_children():
        widget.destroy()

    playlists = fetch_playlists()

    for i,playlist_name in enumerate(playlists):

        playlist_button = Button(
            playlist_frame,
            text=playlist_name,
            font=("Arial", 14, "bold"),
            fg='#845162',
            # bg='#50184A',
            activebackground='#845162',
            activeforeground='#845162',
            command=lambda name=playlist_name: print(f"Selected playlist: {name}")
        )
        playlist_button.grid(row=i, column=0, sticky="ew", padx=0, pady=1)

        menu_button = Button(
            playlist_frame,
            text=">",
            font=("Arial", 14, "bold"),
            fg="#845162",
            bg="#845162",
            activebackground="#845162",
            activeforeground="#845162"
        )
        menu_button.grid(row=i, column=1, sticky="e", padx=(0, 5), pady=1)

        menu_button.bind("<Button-1>", lambda event, name=playlist_name: show_playlist_menu(
            event, name, playlist_frame, delete_playlist_callback, change_cover_callback
        ))
    playlist_frame.columnconfigure(0, weight=1)
    playlist_frame.columnconfigure(1, weight=0) 




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
        update_playlist_buttons(playlist_frame, delete_playlist, change_playlist_cover)
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

