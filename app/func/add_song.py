import os
import time
from tkinter import filedialog, messagebox
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB
from pydub import AudioSegment
import mysql.connector
from app.db.database import create_connection
from app.func.playlist_handler import create_playlist

def insert_song(connection, user_id, title, artist, album, genre, file_path, cover_path):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO songs (user_id, title, artist, album, genre, file_path, cover_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        values = (user_id, title, artist, album, genre, file_path, cover_path)
        cursor.execute(query, values)
        connection.commit()
        print("Song inserted successfully into songs table.")
    except mysql.connector.Error as e:
        print(f"Error while inserting song: {e}")
    finally:
        cursor.close()

def add_song():
    user_id = 1

    choice = messagebox.askyesno("Add Song", "Do you want to add all songs from a folder?\n"
                                            "Yes - Select a folder\nNo - Select a single song file")
    try:
        connection = create_connection()
        if not connection:
            messagebox.showerror("Error", "Failed to connect to the database.")
            return

        cursor = connection.cursor()
        cursor.execute("SELECT playlist_id FROM playlists WHERE name = 'Local Songs'")
        playlist = cursor.fetchone()

        if not playlist:
            cursor.execute("""
                INSERT INTO playlists (user_id, name, description, created_at, created_by, playlist_cover_path)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (1, "Local Songs", "Your local songs", time.strftime('%Y-%m-%d %H:%M:%S'), 'system',
                  '/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/app/gui/assets/covers/song_covers/song_cover.png'))
            connection.commit()
            playlist_id = cursor.lastrowid
        else:
            playlist_id = playlist[0]

        if choice:
            folder_path = filedialog.askdirectory(title="Select Music Folder")
            if folder_path:
                print(f"Selected folder: {folder_path}")
                create_playlist(user_id, folder_path, insert_song)
                messagebox.showinfo("Success", "All songs from the folder were added successfully!")
            else:
                messagebox.showinfo("Info", "No folder selected.")
        else:
            file_path = filedialog.askopenfilename(
                title="Select a music file",
                filetypes=(("MP3 Files", "*.mp3"), ("WAV Files", "*.wav"))
            )
            if not file_path:
                messagebox.showinfo("Info", "No file selected.")
                return

            title = "Unknown Title"
            artist = "Unknown Artist"
            album = "Unknown Album"
            genre = "Unknown Genre"

            if file_path.endswith(".mp3"):
                audio = MP3(file_path, ID3=ID3)
                tags = audio.tags
                title = tags.get('TIT2', 'Unknown Title').text[0] if 'TIT2' in tags else os.path.basename(file_path)
                artist = tags.get('TPE1', 'Unknown Artist').text[0] if 'TPE1' in tags else "Unknown Artist"
                album = tags.get('TALB', 'Unknown Album').text[0] if 'TALB' in tags else "Unknown Album"

            elif file_path.endswith(".wav"):
                audio = AudioSegment.from_file(file_path, format="wav")
                title = os.path.basename(file_path).split('.')[0]

            cover_path = '/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/app/gui/assets/covers/song_covers/song_cover.png'
            insert_song(connection, user_id, title, artist, album, genre, file_path, cover_path)

            song_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO playlist_songs (playlist_id, song_id)
                VALUES (%s, %s)
            """, (playlist_id, song_id))
            connection.commit()

            messagebox.showinfo("Success", f"Song '{title}' by '{artist}' added successfully!")

    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Failed to add song: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
