import tkinter as tk
from tkinter import messagebox
from app.func.authentication import register_user

def create_register_window(connection, on_register_success):
    register_root = tk.Tk()
    register_root.title("WaveForm")
    register_root.geometry("500x500")
    register_root.configure(bg="#1E052A")

    tk.Label(
        register_root, 
        text="Register for WaveForm", 
        font=("Arial", 18, "bold"), 
        fg="white", 
        bg="#1E052A"
    ).pack(pady=20)

    username_label = tk.Label(
        register_root, 
        text="Username", 
        fg="white", 
        bg="#1E052A", 
        font=("Arial", 12)
    )
    username_label.pack(pady=5)
    username_entry = tk.Entry(register_root, font=("Arial", 12), width=30)
    username_entry.pack(pady=5)

    password_label = tk.Label(
        register_root, 
        text="Password", 
        fg="white", 
        bg="#1E052A", 
        font=("Arial", 12)
    )
    password_label.pack(pady=5)
    password_entry = tk.Entry(register_root, show="*", font=("Arial", 12), width=30)
    password_entry.pack(pady=5)

    confirm_password_label = tk.Label(
        register_root, 
        text="Confirm Password", 
        fg="white", 
        bg="#1E052A", 
        font=("Arial", 12)
    )
    confirm_password_label.pack(pady=5)
    confirm_password_entry = tk.Entry(register_root, show="*", font=("Arial", 12), width=30)
    confirm_password_entry.pack(pady=5)

    def handle_register():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if register_user(connection, username, password):  
            messagebox.showinfo("Success", "Account created successfully!")
            register_root.destroy()  
            on_register_success()
        else:
            messagebox.showerror("Error", "Registration failed. Try again.")

    register_button = tk.Button(
        register_root, 
        text="Register", 
        command=handle_register, 
        font=("Arial", 14), 
        bg="#501908", 
        fg="#1E052A"
    )
    register_button.pack(pady=20)

    register_root.mainloop()
