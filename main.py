from tkinter import *
from app.gui.app_window import create_app_window
from app.db.database import create_connection
from app.gui.panels.register_window import create_register_window
from app.gui.panels.init_page import create_init_page
from app.gui.login_window import create_login_window

def main():
    connection = create_connection()
    if not connection:
        print("Error! Unable to connect to database")
        return

    def on_login_success():
        root = create_app_window()
        root.mainloop()

    def on_login():
        create_login_window(connection, on_login_success, on_register)

    def on_register():
        create_register_window(connection, on_login)
        
    def auto_login():
        username = "xmilov3"
        password_hash = "admin"
        
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
        cursor.execute(query, (username, password_hash))
        user = cursor.fetchone()
        
        if user:
            print("Auto-login successful")
            on_login_success()
            return True
        else:
            print("Auto-login failed. Invalid credentials.")
            return False

    if not auto_login():
        create_init_page(
            on_signup=on_register,
            on_signin=on_login
        )

if __name__ == "__main__":
    main()