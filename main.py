import os
from tkinter import *
from app.gui.app_window import create_app_window
from app.db.database import create_connection
from app.gui.panels.register_window import create_register_window
from app.gui.panels.init_page import create_init_page
from app.gui.login_window import create_login_window
from app.func.config import *
from app.gui.assets.pics import *
from app.func.session import user_session


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    connection = create_connection()
    if not connection:
        print("Error! Unable to connect to database")
        return

    def on_login_success():
        user_id = 1
        username = "xmilov3"
        
        user_session.set_user(user_id, username)
        print(f"Session started for user: {username} (ID: {user_id})")
        
        root = create_app_window()
        root.mainloop()

    def on_login():
        create_login_window(connection, on_login_success, on_register)

    def on_register():
        create_register_window(connection, on_login)

    create_init_page(
        on_signup=on_register,
        on_signin=on_login
    )

if __name__ == "__main__":
    main()
