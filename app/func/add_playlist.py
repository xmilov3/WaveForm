import os
from app.db.database import create_connection
from app.func.session import user_session, center_window
from app.func.add_song import insert_song
from tkinter import filedialog, simpledialog, messagebox
from app.func.playlist_handler import delete_playlist, create_playlist
from app.func.playlist_utils import update_playlist_buttons, change_playlist_cover
from app.func.playlist_utils import process_playlist_from_folder
from tkinter import *





def create_empty_playlist(playlist_frame, page_manager):
    user_id = user_session.user_id
    created_by = user_session.username

    dialog = Toplevel()
    dialog.title("Create Playlist")
    center_window(dialog, 500, 300)

    Label(dialog, text="Playlist Name:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=10)
    playlist_name_entry = Entry(dialog, font=("Arial", 12))
    playlist_name_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

    Label(dialog, text="Description:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=10)
    description_entry = Entry(dialog, font=("Arial", 12))
    description_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

    Label(dialog, text="Cover Path:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=10)
    cover_path_entry = Entry(dialog, font=("Arial", 12))
    cover_path_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")



    def browse_cover():
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")]
        )
        if file_path:
            cover_path_entry.delete(0, END)
            cover_path_entry.insert(0, file_path)

    Button(dialog, text="Browse", command=browse_cover).grid(row=2, column=2, padx=10, pady=10)

    def submit_playlist():
        playlist_name = playlist_name_entry.get().strip()
        description = description_entry.get().strip()
        cover_path = cover_path_entry.get().strip()

        if not cover_path:
            cover_path = "app/gui/assets/covers/playlist_covers/default_cover.png"

        if not playlist_name:
            messagebox.showerror("Error", "Playlist name is required!")
            return

        try:
            connection = create_connection()
            cursor = connection.cursor()
            query = """
                INSERT INTO playlists (user_id, name, description, created_by, playlist_cover_path)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, playlist_name, description, created_by, cover_path))
            connection.commit()

            messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully!")
            update_playlist_buttons(playlist_frame, delete_playlist, change_playlist_cover, page_manager)

            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create playlist: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()


    Button(dialog, text="OK", command=submit_playlist).grid(row=3, column=1, sticky="e", padx=10, pady=20)

    Button(dialog, text="Cancel", command=dialog.destroy).grid(row=3, column=2, sticky="w", padx=10, pady=20)

    dialog.columnconfigure(1, weight=1)
    dialog.mainloop()


def import_playlist_from_folder(playlist_frame, page_manager):
    user_id = user_session.user_id
    created_by = user_session.username

    dialog = Toplevel()
    dialog.title("Import Playlist")
    center_window(dialog, 500, 300)
    dialog.configure(bg="#1E052A")

    Label(dialog, text="Playlist Name:", font=("Arial", 12, "bold"), fg="white", bg="#1E052A").grid(row=0, column=0, sticky="w", padx=10, pady=10)
    playlist_name_entry = Entry(dialog, font=("Arial", 12))
    playlist_name_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

    Label(dialog, text="Description:", font=("Arial", 12, "bold"), fg="white", bg="#1E052A").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    description_entry = Entry(dialog, font=("Arial", 12))
    description_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

    Label(dialog, text="Folder Path:", font=("Arial", 12, "bold"), fg="white", bg="#1E052A").grid(row=2, column=0, sticky="w", padx=10, pady=10)
    folder_path_entry = Entry(dialog, font=("Arial", 12))
    folder_path_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    def browse_folder():
        folder_path = filedialog.askdirectory(title="Select Folder with Songs")
        if folder_path:
            folder_path_entry.delete(0, END)
            folder_path_entry.insert(0, folder_path)

    Button(dialog, text="Browse", command=browse_folder).grid(row=2, column=2, padx=10, pady=10)

    Label(dialog, text="Cover Path:", font=("Arial", 12, "bold"), fg="white", bg="#1E052A").grid(row=3, column=0, sticky="w", padx=10, pady=10)
    cover_path_entry = Entry(dialog, font=("Arial", 12))
    cover_path_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    def browse_cover():
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")]
        )
        if file_path:
            cover_path_entry.delete(0, END)
            cover_path_entry.insert(0, file_path)

    Button(dialog, text="Browse", command=browse_cover).grid(row=3, column=2, padx=10, pady=10)

    def submit_import():
        playlist_name = playlist_name_entry.get().strip()
        description = description_entry.get().strip()
        folder_path = folder_path_entry.get().strip()
        cover_path = cover_path_entry.get().strip()

        if not cover_path:
            cover_path = "app/gui/assets/covers/playlist_covers/default_cover.png"

        if not playlist_name:
            messagebox.showerror("Error", "Playlist name is required!")
            return
        if not folder_path:
            messagebox.showerror("Error", "Folder path is required!")
            return

        try:
            print(f"Importing playlist '{playlist_name}' from folder '{folder_path}'")
            playlist_id = process_playlist_from_folder(folder_path, playlist_name, user_id, created_by, insert_song, cover_path)

            if playlist_id:
                messagebox.showinfo("Success", f"Playlist '{playlist_name}' imported successfully!")
                update_playlist_buttons(playlist_frame, delete_playlist, change_playlist_cover, page_manager)
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to import playlist due to database error.")
        except Exception as e:
            print(f"Error importing playlist: {e}")
            messagebox.showerror("Error", f"Failed to import playlist: {e}")

    Button(dialog, text="OK", command=submit_import).grid(row=4, column=1, sticky="e", padx=10, pady=20)
    Button(dialog, text="Cancel", command=dialog.destroy).grid(row=4, column=2, sticky="w", padx=10, pady=20)

    dialog.columnconfigure(1, weight=1)

    dialog.mainloop()
