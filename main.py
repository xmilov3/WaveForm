from tkinter import *
from PIL import Image, ImageTk
from app.gui.app_window import create_app_window
from app.db.database import create_connection
from app.func.config import *
from app.gui.login_window import create_login_window

def main():
    connection = create_connection()
    if not connection:
        print("Error! Unable to connect to database")
        return
    def login_success():
        root = create_app_window()
    
        def on_closing():
            print("Closing database connection")
            connection.close
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    create_login_window(connection, login_success)
    
if __name__ == "__main__":
    main()
