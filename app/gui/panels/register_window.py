import tkinter as tk
from tkinter import messagebox
from app.func.load_pic_gui import *
from datetime import date
from app.func.authentication import register_user
from app.func.session import center_window

def create_register_window(connection, on_register_success):
    register_root = tk.Tk()
    register_root.title("WaveForm")
    center_window(register_root,1500, 1000)
    register_root.configure(bg="#1E052A")
    register_root.iconphoto(False, load_top_logo())

    tk.Label(
        register_root,
        text="WaveForm",
        font=("Arial", 48, "bold"),
        fg="#FFFFFF",
        bg="#1E052A"
    ).pack(pady=20)

    username_label = tk.Label(
        register_root,
        text="Username",
        fg="gray",
        bg="#1E052A",
        font=("Arial", 18)
    )
    username_label.pack(pady=10)
    username_entry = tk.Entry(
        register_root,
        font=("Arial", 16),
        width=30
    )
    username_entry.pack(pady=10)

    email_label = tk.Label(
        register_root,
        text="Email",
        fg="gray",
        bg="#1E052A",
        font=("Arial", 18)
    )
    email_label.pack(pady=10)
    email_entry = tk.Entry(
        register_root,
        font=("Arial", 16),
        width=30
    )
    email_entry.pack(pady=10)

    password_label = tk.Label(
        register_root,
        text="Password",
        fg="gray",
        bg="#1E052A",
        font=("Arial", 18)
    )
    password_label.pack(pady=10)
    password_entry = tk.Entry(
        register_root,
        show="*",
        font=("Arial", 16),
        width=30
    )
    password_entry.pack(pady=10)

    confirm_password_label = tk.Label(
        register_root,
        text="Confirm Password",
        fg="gray",
        bg="#1E052A",
        font=("Arial", 18)
    )
    confirm_password_label.pack(pady=10)
    confirm_password_entry = tk.Entry(
        register_root,
        show="*",
        font=("Arial", 16),
        width=30
    )
    confirm_password_entry.pack(pady=10)

    tk.Label(
        register_root,
        text="Date of Birth",
        fg="gray",
        bg="#1E052A",
        font=("Arial", 18)
    ).pack(pady=10)

    year_var = tk.StringVar(value="Year")
    year_menu = tk.OptionMenu(register_root, year_var, *[str(y) for y in range(1900, date.today().year + 1)])
    year_menu.config(bg="gray", fg="black", font=("Arial", 12))
    year_menu.pack()

    month_var = tk.StringVar(value="Month")
    month_menu = tk.OptionMenu(register_root, month_var, *[str(m).zfill(2) for m in range(1, 13)])
    month_menu.config(bg="gray", fg="black", font=("Arial", 12))
    month_menu.pack()

    day_var = tk.StringVar(value="Day")
    day_menu = tk.OptionMenu(register_root, day_var, *[str(d).zfill(2) for d in range(1, 32)])
    day_menu.config(bg="gray", fg="black", font=("Arial", 12))
    day_menu.pack()

    tk.Label(
        register_root,
        text="Gender",
        fg="gray",
        bg="#1E052A",
        font=("Arial", 18)
    ).pack(pady=10)

    gender_var = tk.StringVar(value="Select Gender")
    gender_menu = tk.OptionMenu(register_root, gender_var, "men", "women")
    gender_menu.pack()


    def handle_register():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        birth_year = year_var.get()
        birth_month = month_var.get()
        birth_day = day_var.get()
        gender = gender_var.get()

        if not username or not email or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if "Year" in birth_year or "Month" in birth_month or "Day" in birth_day:
            messagebox.showerror("Error", "Please select a valid date!")
            return

        if gender == "Select Gender":
            messagebox.showerror("Error", "Please select your gender!")
            return

        birth_date = f"{birth_year}-{birth_month}-{birth_day}"

        try:
            if register_user(connection, username, email, password, birth_date, gender):  
                messagebox.showinfo("Success", "Account created successfully!")
                register_root.destroy()  
                on_register_success()
            else:
                messagebox.showerror("Error", "Registration failed. Try again.")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")

    register_button = tk.Button(
        register_root,
        text="Register",
        font=("Arial", 18, "bold"),
        bg="#9C27B0",
        fg="black",
        width=20,
        height=2,
        command=handle_register
    )
    register_button.pack(pady=30)

    def open_login():
        register_root.destroy()
        on_register_success()

    login_label = tk.Label(
        register_root,
        text="Already have an account? ",
        font=("Arial", 16),
        fg="gray",
        bg="#1E052A"
    )
    login_label.pack(side="left", padx=(580, 0))

    login_link = tk.Label(
        register_root,
        text="Login to WaveForm",
        font=("Arial", 16, "underline"),
        fg="#9C27B0",
        bg="#1E052A",
        cursor="hand2"
    )
    login_link.pack(side="left")
    login_link.bind("<Button-1>", lambda e: open_login())

    register_root.mainloop()
