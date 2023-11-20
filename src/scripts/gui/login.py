import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import sv_ttk
from PIL import ImageTk, Image

from scripts.database.queries import DatabaseManager


class Login(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # Set styles
        self.master.configure_styles()

        # Set theme
        sv_ttk.use_dark_theme()

        # background image
        img = Image.open("../../res/login-background.png").resize((1350, 850))
        self.background_image = ImageTk.PhotoImage(img)  # Keep a reference to the image object

        # Create form frame
        form_frame = ttk.Label(self, image=self.background_image)
        form_frame.pack(side="bottom", fill="both", expand=True)

        # Create username label and entry
        self.username_entry = ttk.Entry(form_frame, width=35, font=('Helvetica', 11, 'normal'))
        self.username_entry.insert(0, 'Username')
        self.username_entry.bind('<FocusIn>', self.clear_username)
        self.username_entry.bind('<FocusOut>', self.fill_username)
        self.username_entry.place(relx=0.51, rely=0.55, anchor='center')

        # Create password label and entry
        self.password_entry = ttk.Entry(form_frame, width=35, font=('Helvetica', 11, 'normal'))
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', self.clear_password)
        self.password_entry.bind('<FocusOut>', self.fill_password)
        self.password_entry.place(relx=0.51, rely=0.65, anchor='center')

        # remember_me = tk.IntVar()
        # remember_me_check = ttk.Checkbutton(form_frame, text='Remember me', variable=remember_me)
        # remember_me_check.place(relx=0.5, rely=0.7, anchor='center')

        style = ttk.Style()
        style.configure('Custom.TButton', font=('Helvetica', 11, 'normal'))

        # Create login button
        login_button = ttk.Button(form_frame, text='Login', width=15, command=self.check_credentials,
                                  style='Custom.TButton', cursor='hand2')
        login_button.place(relx=0.51, rely=0.72, anchor='center')

        # Create forgot password link
        forgot_password_link = ttk.Label(form_frame, text='Forgot password?', cursor='hand2',
                                         font=('Helvetica', 10, 'normal', 'underline'))
        forgot_password_link.place(relx=0.51, rely=0.78, anchor='center')
        forgot_password_link.bind("<Button-1>", self.forgot_password)

    def clear_username(self, event):
        if self.username_entry.get() == 'Username':
            self.username_entry.delete(0, tk.END)

    def fill_username(self, event):
        if self.username_entry.get() == '':
            self.username_entry.insert(0, 'Username')

    def clear_password(self, event):
        if self.password_entry.get() == 'Password':
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(show='*')

    def fill_password(self, event):
        if self.password_entry.get() == '':
            self.password_entry.insert(0, 'Password')
            self.password_entry.config(show='')

    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = DatabaseManager().get_credentials(username, password)

        # Check if username and password are correct
        if user_id:
            full_name = DatabaseManager().get_staff_name(user_id)
            first_name = full_name.split(' ')[0]  # This will get the first name
            self.master.raise_frame('dashboard', first_name)
        else:
            messagebox.showerror('Login error', 'Incorrect username or password')

    @staticmethod
    def forgot_password(event=None):
        messagebox.showinfo('Forgot Password', 'Please contact the system administrator.')
