from tkinter import *
from app.gui.app_window import create_app_window
from app.gui.panels.init_page import create_init_page  # Zmieniono nazwę pliku
from app.gui.login_window import create_login_window
from app.gui.panels.register_window import create_register_window
from app.db.database import create_connection
from app.func.config import *

def main():
    connection = create_connection()
    if not connection:
        print("Error! Unable to connect to database")
        return

    def start_init_page():
        create_init_page(
            on_signup=lambda: create_register_window(connection, start_init_page),
            on_signin=lambda: create_login_window(connection, login_success)
        )

    def login_success():
        root = create_app_window()
    
        def on_closing():
            print("Closing database connection")
            connection.close()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

    start_init_page()

if __name__ == "__main__":
    main()
