import os
from tkinter import messagebox, Menu, Frame, Button, filedialog, Label
from PIL import Image, ImageTk
import mysql.connector
from app.db.database import create_connection

def fetch_playlists():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM playlists")
        playlists = [row[0] for row in cursor.fetchall()]
        return playlists
    except Exception as e:
        print(f"Error downloading playlists: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def fetch_playlist_details(playlist_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="WaveForm_db",
            user="root",
            password=""
        )
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
        if connection.is_connected():
            cursor.close()
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


def split_title_and_artist(file_name):
    try:
        base_name = os.path.splitext(file_name)[0]
        parts = base_name.split(" - ", 1)
        if len(parts) == 2:
            artist_name = parts[0].strip()
            song_title = parts[1].strip()
        else:
            artist_name = "Uknown artist"
            song_title = base_name.strip()
        return song_title, artist_name
    except Exception as e:
        print(f"Error while splitting: {e}")
        return "Unknown album", "Uknown artist"

def process_playlist_from_folder(folder_path, playlist_name, user_id, created_by, insert_song_function):
    connection = create_connection()
    if not connection:
        print("Cannot connect to database.")
        return None

    playlist_id = None
    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO playlists (user_id, name, description, created_by, playlist_cover_path)
            VALUES (%s, %s, %s, %s, %s)
        """
        cover_path = "app/gui/assets/covers/default_cover.png"
        cursor.execute(query, (user_id, playlist_name, "Importing playlist", created_by, cover_path))
        connection.commit()
        playlist_id = cursor.lastrowid

        files = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.wav'))]
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            title, artist = split_title_and_artist(file_name)

            song_id = insert_song_function(
                connection,
                user_id=user_id,
                title=title,
                artist=artist,
                album=playlist_name,
                genre="Unknown Genre",
                file_path=file_path,
                cover_path=cover_path
            )

            if song_id:
                cursor.execute(
                    "INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)",
                    (playlist_id, song_id)
                )
                connection.commit()
                print(f"Added '{title}' by '{artist}' to '{playlist_name}'")
        return playlist_id
    except Exception as e:
        print(f"Playlist processing error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    return playlist_id

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
            messagebox.showerror("Error", "Failed to connect to database.")
            return
        
        cursor = connection.cursor()
        query = "DELETE FROM playlists WHERE name = %s"
        cursor.execute(query, (playlist_name,))
        connection.commit()
        
        messagebox.showinfo("Success", f"Playlist '{playlist_name}' got removed!")
        update_playlist_buttons(playlist_frame, delete_playlist, change_playlist_cover, page_manager)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete playlist: {e}")
    finally:
        if connection and connection.is_connected():
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
