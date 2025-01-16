import unittest
import time
import cProfile
import pstats
import io
from memory_profiler import profile
import psutil
import os
import tkinter as tk
from app.func.authentication import authenticate_user
from app.func.playlist_handler import process_playlist_from_folder
from app.func.music_controller import play_pause_song, next_song
from app.func.add_song import add_song_to_playlist
import mysql.connector

class PerformanceTests(unittest.TestCase):
    def setUp(self):
        self.connection = mysql.connector.connect(
            host='mysql',
            database='WaveForm_db',
            user='root',
            password=''
        )
        self.start_memory = psutil.Process(os.getpid()).memory_info().rss

    # Decorator to measure the execution time of a function
    def measure_execution_time(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"{func.__name__} execution time: {execution_time:.4f} seconds")
            return result
        return wrapper


    # 100 Logins loop
    @measure_execution_time
    def test_login_performance(self):
        for _ in range(100):
            authenticate_user(self.connection, 'testuser', 'testpass123')

    @measure_execution_time
    @profile
    def test_playlist_import_performance(self):
        profiler = cProfile.Profile()
        profiler.enable()
        
        # Symulate importing playlist from folder
        process_playlist_from_folder(
            folder_path="/Users/bartek/Desktop/Muzyka/DJ/DNB",
            playlist_name='Performance Test Playlist',
            user_id=1,
            created_by='testuser',
            insert_song_function=self.mock_insert_song,
            cover_path="/Users/bartek/Desktop/PICS/XD.jpg"
        )
        
        profiler.disable()
        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        stats.print_stats()
        print(s.getvalue())

    @measure_execution_time
    def test_gui_responsiveness(self):
        root = tk.Tk()
        start_time = time.time()
        
        # Symulate creating and destroying frames
        for _ in range(100):
            frame = tk.Frame(root)
            frame.pack()
            label = tk.Label(frame, text="Test")
            label.pack()
            root.update()
            frame.destroy()
        
        end_time = time.time()
        root.destroy()
        
        avg_operation_time = (end_time - start_time) / 100
        self.assertLess(avg_operation_time, 0.1, "GUI operations are too slow")


    def test_memory_usage(self):
        initial_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB
        
        large_playlist = ['song' + str(i) for i in range(1000)]
        for song in large_playlist:
            add_song_to_playlist(f"/path/to/{song}.mp3", "Test Playlist")
        
        final_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Memory usage increased by: {memory_increase:.2f} MB")
        self.assertLess(memory_increase, 100, "Memory usage is too high")

    def test_database_performance(self):
        cursor = self.connection.cursor()
        
        start_time = time.time()
        for i in range(100):
            cursor.execute("SELECT * FROM playlists WHERE user_id = %s", (1,))
            cursor.fetchall()
        
        query_time = (time.time() - start_time) / 100
        print(f"Average query time: {query_time:.4f} seconds")
        self.assertLess(query_time, 0.01, "Database queries are too slow")

    def tearDown(self):
        end_memory = psutil.Process(os.getpid()).memory_info().rss
        memory_diff = end_memory - self.start_memory
        print(f"Memory difference after test: {memory_diff / 1024 / 1024:.2f} MB")
        
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()

        # Mock for the insert_song_function in playlist import test
    def mock_insert_song(self, *args, **kwargs):
        return 1

if __name__ == '__main__':
    unittest.main()