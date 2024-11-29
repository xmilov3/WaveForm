from tkinter import *
from PIL import Image, ImageTk  
import mysql.connector

def fetch_playlist_details(playlist_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''  
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

        if details:
            print(f"Playlist details fetched: {details}")
        else:
            print(f"No details found for playlist: {playlist_name}")

        return details
    except mysql.connector.Error as e:
        print(f"Error while fetching playlist details: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def fetch_songs_by_playlist(playlist_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root', 
            password='' 
        )
        cursor = connection.cursor()

        cursor.execute("SELECT playlist_id FROM playlists WHERE name = %s", (playlist_name,))
        playlist = cursor.fetchone()
        if not playlist:
            print("Playlist not found:", playlist_name)
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

        print(f"Fetched songs for playlist '{playlist_name}': {songs}")
        return songs
    except mysql.connector.Error as e:
        print(f"Error while fetching songs: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_header(header_label, header_image_label, user_label, song_count_label, playlist_name):
    details = fetch_playlist_details(playlist_name)
    if details:
        name, description, cover_path, created_by, song_count = details

        header_label.config(text=name)

        user_label.config(text=f"By {created_by}")

        song_count_label.config(text=f"{song_count} songs")

        if cover_path and cover_path.strip():
            try:
                img = Image.open(cover_path)
                img = img.resize((200, 200), Image.LANCZOS) 
                cover_image = ImageTk.PhotoImage(img)
                header_image_label.config(image=cover_image)
                header_image_label.image = cover_image  
            except Exception as e:
                print(f"Error loading cover image: {e}")
                header_image_label.config(image='') 
        else:
            header_image_label.config(image='')  
    else:
        print("No details available to update header.")
        header_label.config(text="Unknown Playlist") 
        user_label.config(text="Unknown Author")  
        song_count_label.config(text="0 songs")  
        header_image_label.config(image='') 



def update_song_listbox(song_listbox, playlist_name):
    songs = fetch_songs_by_playlist(playlist_name)
    song_listbox.delete(0, END) 
    if not songs:
        song_listbox.insert(END, "No songs found.")
    else:
        for song in songs:
            title, artist = song
            song_listbox.insert(END, f"{title} - {artist}")

def create_middle_panel(parent):
    middle_frame = Frame(parent, bg='#3C0F64')
    middle_frame.grid(row=1, column=1, sticky='nsew', padx=1, pady=1)

    header_frame = Frame(middle_frame, bg='#3A0C60')
    header_frame.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)

    header_image_label = Label(header_frame, bg='#3A0C60')
    header_image_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky='nw')

    header_label = Label(header_frame, text='', font=("Arial", 54, "bold"), fg='white', bg='#3A0C60')
    header_label.grid(row=0, column=1, sticky="nw", padx=(10, 0), pady=(0, 0))

    user_label = Label(header_frame, text='', font=("Arial", 14), fg='white', bg='#3A0C60')
    user_label.grid(row=1, column=1, sticky="w", padx=(10, 0))

    song_count_label = Label(header_frame, text='', font=("Arial", 12), fg='white', bg='#3A0C60')
    song_count_label.grid(row=2, column=1, sticky="w", padx=(10, 0))

    songlist_frame = Frame(middle_frame, bg='white')
    songlist_frame.grid(row=1, column=0, sticky='nsew', padx=0, pady=0)

    song_listbox = Listbox(songlist_frame, bg='#3A0C60', fg='black', font=("Arial", 18), selectbackground="#3A0C60")
    song_listbox.pack(fill=BOTH, expand=True)

    update_header(header_label, header_image_label, user_label, song_count_label, "liked Songs")
    update_song_listbox(song_listbox, "Liked Songs")

    return middle_frame, song_listbox
