import tkinter as tk
from tkinter import messagebox
from app.func.load_pic_gui import load_top_logo, load_init_logo
from app.func.authentication import authenticate_user
from app.func.session import center_window, user_session

class LoginPage(tk.Frame):
    def __init__(self, parent, page_manager, connection):
        super().__init__(parent, bg="#1E052A")
        self.page_manager = page_manager
        self.connection = connection

        self.configure(bg="#1E052A")


        init_logo = load_init_logo()
        logo_label = tk.Label(
            self,
            image=init_logo,
            bg="#1E052A"
        )
        logo_label.image = init_logo
        logo_label.pack()

        tk.Label(self, text="Username", fg="gray", bg="#1E052A", font=("Arial", 18)).pack(pady=10)
        self.username_entry = tk.Entry(self, font=("Arial", 16), width=30)
        self.username_entry.pack(pady=10)

        tk.Label(self, text="Password", fg="gray", bg="#1E052A", font=("Arial", 18)).pack(pady=10)
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 16), width=30)
        self.password_entry.pack(pady=10)

        login_button = tk.Button(
            self,
            text="Login",
            font=("Arial", 18, "bold"),
            bg="#9C27B0",
            fg="black",
            width=20,
            height=2,
            command=self.handle_login
        )
        login_button.pack(pady=30)

        tk.Label(self, text="Don't have an account?", font=("Arial", 16), fg="gray", bg="#1E052A").pack()
        register_link = tk.Label(
            self,
            text="Register to WaveForm",
            font=("Arial", 16, "underline"),
            fg="#9C27B0",
            bg="#1E052A",
            cursor="hand2"
        )
        register_link.pack(pady=(5, 20))
        register_link.bind("<Button-1>", lambda e: self.page_manager.show_page("RegisterPage"))

        self.update_idletasks()

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            cursor = self.connection.cursor()
            query = "SELECT user_id, username FROM users WHERE username = %s AND password_hash = %s"
            cursor.execute(query, (username, password))
            user_data = cursor.fetchone()

            if user_data:
                user_id, username = user_data
                user_session.set_user(user_id, username)
                print(f"User logged in: {username} (ID: {user_id})")
                self.page_manager.show_page("AppWindow")
            else:
                print("Invalid login credentials.")
                messagebox.showerror("Login Failed", "Invalid credentials.")
        except Exception as e:
            print(f"Error during login: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if cursor:
                cursor.close()