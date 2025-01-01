import os
from tkinter import Menu, Button, messagebox, filedialog
from PIL import Image, ImageTk
import mysql.connector
from app.db.database import create_connection
from app.func.playlist_handler import process_playlist_from_folder
from tkinter import Button, Menu
from app.func.playlist_handler import fetch_playlists


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="WaveForm_db",
            user="root",
            password=""
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

playlist_buttons = {}

def update_playlist_buttons(playlist_frame, delete_playlist_callback, change_cover_callback, page_manager):
    global playlist_buttons

    playlists = fetch_playlists()

    existing_widgets = {widget.cget("text"): widget for widget in playlist_frame.winfo_children() if isinstance(widget, Button)}

    for playlist_name in list(existing_widgets.keys()):
        if playlist_name not in playlists:
            existing_widgets[playlist_name].destroy()
            if playlist_name in playlist_buttons:
                del playlist_buttons[playlist_name]

    for i, playlist_name in enumerate(playlists):
        if playlist_name in existing_widgets:
            button = existing_widgets[playlist_name]
            button.configure(
                text=playlist_name
            )
        else:
            button = Button(
                playlist_frame,
                text=playlist_name,
                font=("Arial", 14, "bold"),
                # borderwidth=0,
                command=lambda name=playlist_name: page_manager.show_dynamic_panel("MiddlePanel", name)
            )
            button.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
            button.bind("<Button-3>", lambda event, name=playlist_name: show_context_menu(event, name, playlist_frame, page_manager))
            button.bind("<Control-Button-1>", lambda event, name=playlist_name: show_context_menu(event, name, playlist_frame, page_manager))

            playlist_buttons[playlist_name] = button

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



def fetch_playlist_details(playlist_name):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = """
            SELECT p.name, p.description, p.playlist_cover_path, p.created_by, COUNT(ps.song_id)
            FROM playlists p
            LEFT JOIN playlist_songs ps ON p.playlist_id = ps.playlist_id
            WHERE p.name = %s
            GROUP BY p.playlist_id
        """
        cursor.execute(query, (playlist_name,))
        details = cursor.fetchone()
        return details
    except mysql.connector.Error as e:
        print(f"Error getting playlist details '{playlist_name}': {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()



def fetch_songs_by_playlist(playlist_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="WaveForm_db",
            user="root",
            password=""
        )
        cursor = connection.cursor()
        cursor.execute("SELECT playlist_id FROM playlists WHERE name = %s", (playlist_name,))
        playlist = cursor.fetchone()
        if not playlist:
            return []

        playlist_id = playlist[0]
        query = """
            SELECT s.title, s.artist
            FROM songs s
            JOIN playlist_songs ps ON s.song_id = ps.song_id
            WHERE ps.playlist_id = %s
        """
        cursor.execute(query, (playlist_id,))
        songs = cursor.fetchall()
        return songs
    except mysql.connector.Error as e:
        print(f"Error downloading songs: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def load_cover_image(cover_path, label):
    try:
        img = Image.open(cover_path)
        img = img.resize((150, 150), Image.LANCZOS)
        cover_image = ImageTk.PhotoImage(img)
        label.config(image=cover_image)
        label.image = cover_image
    except FileNotFoundError:
        print(f"Image loading error: File not found at path {cover_path}")
        label.config(text="No Cover", fg="white", font=("Arial", 16, "bold"))
    except Exception as e:
        print(f"Image loading error: {e}")
        label.config(text="No Cover", fg="white", font=("Arial", 16, "bold"))


def split_title_and_artist(file_name):
    try:
        base_name = os.path.splitext(file_name)[0]
        parts = base_name.split(" - ", 1)
        if len(parts) == 2:
            artist_name = parts[0].strip()
            song_title = parts[1].strip()
        else:
            artist_name = "Unknown artist"
            song_title = base_name.strip()
        return song_title, artist_name
    except Exception as e:
        print(f"Error while splitting: {e}")
        return "Unknown album", "Unknown artist"


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
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_playlist(playlist_name, playlist_frame, update_function, page_manager):
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
        update_function(playlist_frame, page_manager)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete playlist: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
