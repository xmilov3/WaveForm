from tkinter import *
from tkinter import simpledialog, filedialog, messagebox
from app.func.add_song import add_song
from app.db.db_operations import insert_song
from app.func.add_playlist import create_empty_playlist, import_playlist_from_folder
from app.func.playlist_utils import update_playlist_buttons, change_playlist_cover, delete_playlist, fetch_playlists




def create_left_panel(parent, page_manager):
    left_frame = Frame(parent, bg='#1E052A', borderwidth=0)
    left_frame.grid(row=1, column=0, sticky='nsew')

    buttons_frame = Frame(left_frame, bg='#2d0232')
    buttons_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    playlist_frame = Frame(left_frame, bg='#2d0232')
    playlist_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

    Button(
        buttons_frame,
        text="Add Song",
        font=("Arial", 14, "bold"),
        command=lambda: add_song_with_playlist(page_manager),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0
    ).pack(fill="x", padx=10, pady=5)

    Button(
        buttons_frame,
        text="Create Playlist",
        font=("Arial", 14, "bold"),
        command=lambda: create_empty_playlist(playlist_frame, page_manager),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0
    ).pack(fill="x", padx=10, pady=5)
    
    Button(
        buttons_frame,
        text="Import playlist",
        font=("Arial", 14, "bold"),
        command=lambda: import_playlist_from_folder(playlist_frame, page_manager),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0
    ).pack(fill="x", padx=10, pady=5)


    Button(
        buttons_frame,
        text="Analyze Song",
        font=("Arial", 14, "bold"),
        command=lambda: add_song_with_playlist(page_manager),
        fg='#845162',
        bg='#50184A',
        activebackground='#845162',
        activeforeground='#845162',
        borderwidth=0,
        padx=10, pady=5
    ).pack(fill="x", padx=10, pady=5)

    
    
    populate_playlists(playlist_frame, page_manager)

    return left_frame

def populate_playlists(playlist_frame, page_manager):
    playlists = fetch_playlists()

    listbox = getattr(playlist_frame, "listbox", None)
    if not listbox:
        listbox = Listbox(
            playlist_frame,
            bg="#2D0232",
            fg="white",
            font=("Arial", 14),
            selectbackground="#50184A",
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0
        )
        listbox.pack(fill=BOTH, expand=True, padx=10, pady=10)
        playlist_frame.listbox = listbox

    listbox.delete(0, END)

    if playlists:
        for playlist_name in playlists:
            listbox.insert(END, playlist_name)
        
        listbox.bind(
            "<<ListboxSelect>>",
            lambda event: handle_playlist_selection(event, page_manager, listbox)
        )
    else:
        listbox.insert(END, "No playlists available.")


def handle_playlist_selection(event, page_manager, listbox):
    selected_index = listbox.curselection()  # Pobierz zaznaczenie
    if selected_index:
        playlist_name = listbox.get(selected_index)
        page_manager.show_dynamic_panel("MiddlePanel", playlist_name)



def add_song_with_playlist():
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


def load_playlist_songs(playlist_name):
    from app.db.database import create_connection
    print(f"Loading songs for playlist: {playlist_name}")
    try:
        connection = create_connection()
        if not connection:
            print("Failed to connect to the database.")
            return

        cursor = connection.cursor()
        query = """
            SELECT songs.title, songs.artist 
            FROM songs
            JOIN playlist_songs ON songs.song_id = playlist_songs.song_id
            JOIN playlists ON playlists.playlist_id = playlist_songs.playlist_id
            WHERE playlists.name = %s
        """
        cursor.execute(query, (playlist_name,))
        songs = cursor.fetchall()

        if songs:
            print(f"Songs in '{playlist_name}':")
            for song in songs:
                print(f"Title: {song[0]}, Artist: {song[1]}")
        else:
            print(f"No songs found in playlist '{playlist_name}'.")

    except Exception as e:
        print(f"Error loading playlist songs: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def initialize_middle_frame(playlist_frame, page_manager):
    playlists = fetch_playlists()
    if playlists:
        first_playlist = playlists[0]
        page_manager.show_dynamic_panel("MiddlePanel", first_playlist)
    else:
        print("No songs found to load.")

    update_playlist_buttons(playlist_frame, delete_playlist, change_playlist_cover, page_manager)
    initialize_middle_frame(playlist_frame, page_manager)
