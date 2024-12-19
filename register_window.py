import tkinter as tk
from tkinter import messagebox
from datetime import date
from app.func.load_pic_gui import load_top_logo, load_init_logo
from app.func.authentication import register_user


class RegisterPage(tk.Frame):
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

        self.create_entry("Username", "username_entry")
        self.create_entry("Email", "email_entry")
        self.create_entry("Password", "password_entry", show="*")
        self.create_entry("Confirm Password", "confirm_password_entry", show="*")

        tk.Label(self, text="Date of Birth", font=("Arial", 18), fg="gray", bg="#1E052A").pack(pady=(10, 5))
        self.create_date_of_birth_fields()

        tk.Label(self, text="Gender", font=("Arial", 18), fg="gray", bg="#1E052A").pack(pady=(10, 5))
        self.gender_var = tk.StringVar(value="Select Gender")
        gender_menu = tk.OptionMenu(self, self.gender_var, "Men", "Women")
        gender_menu.config(bg="gray", fg="black", font=("Arial", 12))
        gender_menu.pack(pady=5)

        register_button = tk.Button(
            self,
            text="Register",
            font=("Arial", 18, "bold"),
            bg="#9C27B0",
            fg="black",
            width=20,
            height=2,
            command=self.handle_register
        )
        register_button.pack(pady=20)

        tk.Label(self, text="Already have an account?", font=("Arial", 16), fg="gray", bg="#1E052A").pack()
        login_link = tk.Label(
            self,
            text="Login to WaveForm",
            font=("Arial", 16, "underline"),
            fg="#9C27B0",
            bg="#1E052A",
            cursor="hand2"
        )
        login_link.pack(pady=(5, 20))
        login_link.bind("<Button-1>", lambda e: self.page_manager.show_page("LoginPage"))

    def create_entry(self, label_text, attr_name, show=""):
        tk.Label(self, text=label_text, font=("Arial", 18), fg="gray", bg="#1E052A").pack(pady=(5, 2))
        entry = tk.Entry(self, font=("Arial", 16), show=show, width=30)
        entry.pack(pady=5)
        setattr(self, attr_name, entry)

    def create_date_of_birth_fields(self):
        dob_frame = tk.Frame(self, bg="#1E052A")
        dob_frame.pack(pady=5)

        self.year_var = tk.StringVar(value="Year")
        self.month_var = tk.StringVar(value="Month")
        self.day_var = tk.StringVar(value="Day")

        year_menu = tk.OptionMenu(
            dob_frame, 
            self.year_var, 
            *sorted([str(y) for y in range(1960, date.today().year + 1)], reverse=True)
        )
        month_menu = tk.OptionMenu(dob_frame, self.month_var, *[str(m).zfill(2) for m in range(1, 13)])
        self.day_menu = tk.OptionMenu(dob_frame, self.day_var, "")
        
        for menu in (year_menu, month_menu, self.day_menu):
            menu.config(bg="gray", fg="black", font=("Arial", 12))
            menu.pack(side="left", padx=5)

        self.year_var.trace("w", self.update_days)
        self.month_var.trace("w", self.update_days)
        self.update_days()

    def update_days(self, *args):
        year = self.year_var.get()
        month = self.month_var.get()

        if not year.isdigit() or not month.isdigit():
            days_in_month = range(1, 32)
        else:
            year = int(year)
            month = int(month)
            days_in_month = self.get_days_in_month(year, month)

        menu = self.day_menu["menu"]
        menu.delete(0, "end")

        for day in days_in_month:
            menu.add_command(label=str(day).zfill(2), command=lambda value=str(day).zfill(2): self.day_var.set(value))

        self.day_var.set("Day")

    def get_days_in_month(self, year, month):
        if month in {1, 3, 5, 7, 8, 10, 12}:
            return range(1, 32)
        elif month in {4, 6, 9, 11}:
            return range(1, 31)
        elif month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return range(1, 30)
            else:
                return range(1, 29)
        return range(1, 32)

    def handle_register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        birth_year = self.year_var.get()
        birth_month = self.month_var.get()
        birth_day = self.day_var.get()
        gender = self.gender_var.get()

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
            if register_user(self.connection, username, email, password, birth_date, gender):
                messagebox.showinfo("Success", "Account created successfully!")
                self.page_manager.show_page("LoginPage")
            else:
                messagebox.showerror("Error", "Registration failed. Try again.")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
