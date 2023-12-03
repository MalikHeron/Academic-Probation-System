import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import keyring
import sv_ttk
from PIL import ImageTk, Image

from scripts.database.queries import DatabaseManager
from scripts.gui.helpers import Helpers


class Login(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # Initialize variables
        self.remember_me_field = None
        self.remember_me = None
        self._password_entry = None
        self._username_entry = None
        self._master = master

        # Set theme
        sv_ttk.use_dark_theme()

        # Initialize helpers
        self._helpers = Helpers()

        # Set dark title bar
        self._helpers.set_title_bar_mode(self._master, 2)

        # Set styles
        self.configure_styles()

        # background image
        img = Image.open("../../res/login-background.png")
        img = img.resize((int(master.winfo_width() + 2), int(master.winfo_height() + 2)))
        self._background_image = ImageTk.PhotoImage(img)  # Keep a reference to the image object

        # Create form frame
        self.form_frame = ttk.Label(self, image=self._background_image)
        self.form_frame.pack(side="bottom", fill="both", expand=True)

        self.add_widgets()

        # Bind the <Configure> event to the update_size method
        self.form_frame.bind('<Configure>', self.update_size)

    def update_size(self, event):
        # Resize the image
        img = Image.open("../../res/login-background.png")
        img = img.resize((int(event.width + 2), int(event.height + 2)))
        self._background_image = ImageTk.PhotoImage(img)

        # Update the form_frame widget to use the resized image
        self.form_frame.config(image=self._background_image)

    def add_widgets(self):
        # Create username label and entry
        self._username_entry = ttk.Entry(self.form_frame, width=35, font=('Helvetica', 11, 'normal'))
        self._username_entry.insert(0, 'Username')
        self._username_entry.bind('<FocusIn>', self._clear_username)
        self._username_entry.bind('<FocusOut>', self._fill_username)
        self._username_entry.place(relx=0.5, rely=0.52, anchor='center')

        # Create password label and entry
        self._password_entry = ttk.Entry(self.form_frame, width=35, font=('Helvetica', 11, 'normal'))
        self._password_entry.insert(0, 'Password')
        self._password_entry.bind('<FocusIn>', self._clear_password)
        self._password_entry.bind('<FocusOut>', self._fill_password)
        self._password_entry.place(relx=0.5, rely=0.60, anchor='center')

        self.remember_me = tk.IntVar(value=0)
        self.remember_me_field = ttk.Checkbutton(self.form_frame, text='Remember me', variable=self.remember_me)
        self.remember_me_field.place(relx=0.5, rely=0.66, anchor='center')

        # Create login button
        login_button = ttk.Button(self.form_frame, text='Login', width=15, command=self._check_credentials,
                                  style='TButton', cursor='hand2')
        login_button.place(relx=0.5, rely=0.715, anchor='center')

        # Create forgot password link
        forgot_password_link = ttk.Label(self.form_frame, text='Forgot password?', cursor='hand2',
                                         font=('Helvetica', 10, 'normal', 'underline'))
        forgot_password_link.place(relx=0.5, rely=0.77, anchor='center')
        forgot_password_link.bind("<Button-1>", self.__forgot_password)

        # Load credentials if remember_me file exists
        username = keyring.get_password("AcademicProbationSystem", "username")
        password = keyring.get_password("AcademicProbationSystem", "password")
        if username and password:
            self._username_entry.delete(0, tk.END)
            self._username_entry.insert(0, username)
            self._password_entry.delete(0, tk.END)
            self._password_entry.insert(0, password)

            self._check_credentials()

    def _clear_username(self, event):
        if self._username_entry.get() == 'Username':
            self._username_entry.delete(0, tk.END)

    def _fill_username(self, event):
        if self._username_entry.get() == '':
            self._username_entry.insert(0, 'Username')

    def _clear_password(self, event):
        if self._password_entry.get() == 'Password':
            self._password_entry.delete(0, tk.END)
            self._password_entry.config(show='*')

    def _fill_password(self, event):
        if self._password_entry.get() == '':
            self._password_entry.insert(0, 'Password')
            self._password_entry.config(show='')

    def _check_credentials(self):
        username = self._username_entry.get()
        password = self._password_entry.get()
        user_id = DatabaseManager().get_credentials(username, password)

        # Check if username and password are correct
        if user_id:
            full_name = DatabaseManager().get_staff_name(user_id)
            first_name = full_name.split(' ')[0]  # This will get the first name
            # Raise the dashboard frame
            self.master.raise_frame('dashboard', first_name)

            if self.remember_me.get() == 1:
                # Save credentials if remember_me is checked
                keyring.set_password("AcademicProbationSystem", "username", username)
                keyring.set_password("AcademicProbationSystem", "password", password)
        else:
            messagebox.showerror('Login Error', 'Incorrect username or password.')

    @staticmethod
    def __forgot_password(event=None):
        messagebox.showinfo('Forgot Password', 'Please contact the system administrator.')

    @staticmethod
    def configure_styles():
        # Create a style
        style = ttk.Style()

        # Configure the font style for Button
        style.configure('TButton', font=('Helvetica', 11, 'normal'))

        # Configure the font style for Label
        style.configure('TLabel', font=('Helvetica', 11, 'normal'))

        # Configure the font style for Checkbutton
        style.configure('TCheckbutton', font=('Helvetica', 10, 'normal'))
