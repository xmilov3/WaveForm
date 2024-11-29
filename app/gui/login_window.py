import tkinter as tk
from tkinter import messagebox
from app.func.authentication import authenticate_user

def create_login_window(connection, on_login_success):
    login_root = tk.Tk()
    login_root.title("WaveForm")
    login_root.geometry("500x500")
    login_root.configure(bg="#1E052A")

    tk.Label(
        login_root, 
        text="Login to WaveForm", 
        font=("Arial", 18, "bold"), 
        fg="white", 
        bg="#1E052A"
    ).pack(pady=20)

    username_label = tk.Label(
        login_root, 
        text="Username", 
        fg="white", 
        bg="#1E052A", 
        font=("Arial", 12)
    )
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_root, font=("Arial", 12), width=30)
    username_entry.pack(pady=5)

    password_label = tk.Label(
        login_root, 
        text="Password", 
        fg="white", 
        bg="#1E052A", 
        font=("Arial", 12)
    )
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_root, show="*", font=("Arial", 12), width=30)
    password_entry.pack(pady=5)

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        
        if authenticate_user(connection, username, password):  
            login_root.destroy()  
            on_login_success() 
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

    login_button = tk.Button(
        login_root, 
        text="Login", 
        command=handle_login, 
        font=("Arial", 14), 
        bg="#501908", 
        fg="#1E052A"
    )
    login_button.pack(pady=20)

    login_root.mainloop()
