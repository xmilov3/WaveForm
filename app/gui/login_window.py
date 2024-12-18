import tkinter as tk
from tkinter import messagebox
from app.func.load_pic_gui import *
from app.func.authentication import authenticate_user
from app.func.config import *
from app.func.session import center_window

def create_login_window(connection, on_login_success, on_register):
    login_root = tk.Tk()
    login_root.title("WaveForm")
    center_window(login_root,1500,1000)
    login_root.configure(bg="#1E052A")
    login_root.iconphoto(False, load_top_logo())

    tk.Label(
        login_root,
        text="WaveForm",
        font=("Arial", 48, "bold"),
        fg="#1E052A",
        bg="#1E052A"
    ).pack()

    init_logo = load_init_logo()
    logo_label = tk.Label(
        login_root,
        image=init_logo,
        bg="#1E052A"
    )
    logo_label.image = init_logo
    logo_label.pack()

    username_label = tk.Label(
        login_root,
        text="Username",
        fg="gray",
        bg="#1E052A",
        font=("Arial", 18)
    )
    username_label.pack(pady=10)
    username_entry = tk.Entry(
        login_root,
        font=("Arial", 16),
        width=30
    )
    username_entry.pack(pady=10)

    password_label = tk.Label(
        login_root,
        text="Password",
        fg="gray",
        bg="#1E052A",
        font=("Arial", 18)
    )
    password_label.pack(pady=10)
    password_entry = tk.Entry(
        login_root,
        show="*",
        font=("Arial", 16),
        width=30
    )
    password_entry.pack(pady=10)

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()

        try:
            cursor = connection.cursor()
            query = "SELECT user_id, username FROM users WHERE username = %s AND password_hash = %s"
            cursor.execute(query, (username, password))
            user_data = cursor.fetchone()

            if user_data:
                print("Login successful!")
                login_root.destroy()
                on_login_success(user_data)
            else:
                print("Invalid login credentials.")
                messagebox.showerror("Login Failed", "Invalid email or password.")
        except Exception as e:
            print(f"Error during login: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if cursor:
                cursor.close()

    login_button = tk.Button(
        login_root,
        text="Login",
        font=("Arial", 18, "bold"),
        bg="#9C27B0",
        fg="black",
        width=20,
        height=2,
        command=handle_login
    )
    login_button.pack(pady=30)

    tk.Label(
        login_root,
        text="",
        bg="#1E052A"
    ).pack(pady=20)

    def open_register():
        login_root.destroy()
        on_register()

    register_label = tk.Label(
        login_root,
        text="Don't have an account? ",
        font=("Arial", 16),
        fg="gray",
        bg="#1E052A"
    )
    register_label.pack(side="left", padx=(580, 0))

    register_link = tk.Label(
        login_root,
        text="Register to WaveForm",
        font=("Arial", 16, "underline"),
        fg="#9C27B0",
        bg="#1E052A",
        cursor="hand2"
    )
    register_link.pack(side="left")
    register_link.bind("<Button-1>", lambda e: open_register())

    login_root.mainloop()
