import tkinter as tk
from app.func.load_pic_gui import load_init_logo

def create_init_page(on_signup, on_signin):
    home_root = tk.Tk()
    home_root.title("WaveForm")
    home_root.geometry("1500x1000")
    home_root.configure(bg="#1E052A")

    tk.Label(
        home_root,
        text="WaveForm",
        font=("Arial", 48, "bold"),
        fg="#1E052A",
        bg="#1E052A"
    ).pack()

    init_logo = load_init_logo()  
    logo_label = tk.Label(
        home_root,
        image=init_logo,
        bg="#1E052A"
    )
    logo_label.image = init_logo  
    logo_label.pack()

    tk.Label(
        home_root,
        text="Welcome to WaveForm",
        font=("Arial", 40, "bold"),
        fg="white",
        bg="#1E052A"
    ).pack(pady=50)

    def handle_signup():
        home_root.destroy()
        on_signup()

    def handle_signin():
        home_root.destroy()
        on_signin()

    signup_button = tk.Button(
        home_root,
        text="Sign up",
        font=("Arial", 18, "bold"),
        bg="#9C27B0",
        fg="black",
        width=20,
        height=2,
        command=handle_signup
    )
    signup_button.pack(pady=20)

    tk.Label(
        home_root,
        text="Or",
        font=("Arial", 18),
        fg="white",
        bg="#1E052A"
    ).pack(pady=10)

    signin_button = tk.Button(
        home_root,
        text="Sign in",
        font=("Arial", 18, "bold"),
        bg="#3C0F64",
        fg="black",
        width=20,
        height=2,
        command=handle_signin
    )
    signin_button.pack(pady=20)

    home_root.mainloop()
