import tkinter as tk
from tkinter import *
from app.gui.page_manager import PageManager
from app.gui.init_page import InitPage
from app.gui.app_window import AppWindow
from app.gui.login_window import LoginPage
from app.gui.register_window import RegisterPage
from app.db.database import create_connection
from app.func.session import user_session
from app.gui.panels.middle_panel import create_middle_panel
from app.func.load_pic_gui import load_top_logo

def main():
   root = tk.Tk()
   page_manager = PageManager(root)
   root.withdraw() 
   root.title("WaveForm")
   root.configure(bg="#1E052A")
   root.geometry("1500x1000")
   icon = load_top_logo()
   root.iconphoto(True, icon)
   root.deiconify()

   connection = create_connection()
   if not connection:
       print("Error! Unable to connect to database")
       return
   
   root.grid_rowconfigure(0, weight=1)
   root.grid_columnconfigure(0, weight=1)

   def on_login_success(user_data):
       user_id, username = user_data
       user_session.set_user(user_id, username)
       print(f"Session started for user: {username} (ID: {user_id})")
       page_manager.show_page("AppWindow")
       root.deiconify()

   def auto_login():
       cursor = connection.cursor()
       query = "SELECT user_id, username FROM users WHERE username = %s AND password_hash = %s"
       cursor.execute(query, ("xmilov3", "admin"))
       user = cursor.fetchone()
       cursor.close()

       if user:
           print("Auto-login successful")
           on_login_success(user)
           return True
       return False

   init_page = InitPage(root, page_manager)
   login_page = LoginPage(root, page_manager, connection)
   register_page = RegisterPage(root, page_manager, connection)
   app_window = AppWindow(root, page_manager)
   
   page_manager.current_window = app_window

   page_manager.add_page("InitPage", init_page)
   page_manager.add_page("LoginPage", login_page)
   page_manager.add_page("RegisterPage", register_page)
   page_manager.add_page("AppWindow", app_window)
   
   page_manager.add_dynamic_panel(
       "MiddlePanel",
       lambda parent, playlist_name: create_middle_panel(
           app_window.main_frame,
           playlist_name,
           app_window.title_label,
           app_window.artist_label,
           app_window.album_art_label,
           app_window.time_elapsed_label,
           app_window.time_remaining_label,
           app_window.progress_slider
       )
   )

   auto_login()
   page_manager.center_window(1500, 1000)
   
   root.mainloop()

if __name__ == "__main__":
   main()