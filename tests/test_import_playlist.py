import unittest
from unittest.mock import MagicMock, patch
import mysql.connector
from app.func.session import user_session
import tkinter as tk


class TestPlaylistImportDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Connecting to db")
        cls.connection = mysql.connector.connect(
            host='localhost',
            database='WaveForm_db',
            user='root',
            password=''
        )
        cursor = cls.connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = 'testuser'")
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, birth_date, gender, created_at)
            VALUES ('testuser', 'test@example.com', 'testpass123', '2000-01-01', 'men', CURRENT_TIMESTAMP())
        """)
        cls.connection.commit()
        cls.test_user_id = cursor.lastrowid
        cursor.close()
        print("Test user created")

    def setUp(self):
        print("Starting test environment setup")
        self.root = tk.Tk()
        self.page_manager = MagicMock()
        self.playlist_frame = tk.Frame(self.root)
        
        # Sign in test user
        user_session.set_user(self.__class__.test_user_id, 'testuser')
        print(f"User logged in: ID={self.__class__.test_user_id}, username='testuser'.")

    @patch('tkinter.filedialog.askdirectory')
    @patch('tkinter.filedialog.askopenfilename')
    def test_import_playlist_dialog(self, mock_file_dialog, mock_dir_dialog):
        print("Starting playlist import dialog test")
        # Simulate user selecting paths
        mock_dir_dialog.return_value = "/Users/bartek/Desktop/Muzyka/DJ/DNB/"
        mock_file_dialog.return_value = "/Users/bartek/Desktop/PICS/XD.jpg"

        # Open the import dialog
        from app.func.playlist_handler import process_playlist_from_folder

        # Example arguments for missing parameters
        user_id = self.__class__.test_user_id
        created_by = 'testuser'

        # Create the `insert_song_function` as a simulation
        def insert_song_function(connection, user_id, title, artist, album, genre, file_path, cover_path):
            print(f"Mock insert_song_function called with: {title}, {artist}, {file_path}")
            return 255  # Simulate that the song was added and return its ID

        # Call the function with required arguments
        try:
            playlist_id = process_playlist_from_folder(
                folder_path="/Users/bartek/Desktop/Muzyka/DJ/DNB",
                playlist_name="Test Playlist",
                user_id=user_id,
                created_by=created_by,
                insert_song_function=insert_song_function,  # Correctly pass the function
                cover_path="/Users/bartek/Desktop/PICS/XD.jpg"
            )
            self.assertIsNotNone(playlist_id, "The process_playlist_from_folder function returned None instead of a playlist ID")
            print(f"Test passed! Playlist created with ID: {playlist_id}")
        except Exception as e:
            self.fail(f"process_playlist_from_folder raised an exception: {e}")

    def tearDown(self):
        print("Clearing user session and destroying test environment")
        user_session.clear_session()
        self.root.destroy()

    @classmethod
    # Clean up test user from the database
    def tearDownClass(cls):
        print("Deleting test user from the database")
        cursor = cls.connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = 'testuser'")
        cls.connection.commit()
        cursor.close()
        cls.connection.close()
        print("Test user deleted")


if __name__ == '__main__':
    unittest.main()
