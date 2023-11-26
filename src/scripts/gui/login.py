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
        self.img = Image.open("../../res/login-background.png").resize((1350, 893))
        self._background_image = ImageTk.PhotoImage(self.img)  # Keep a reference to the image object

        # Create a copy of img to later be resized
        self.img_copy = self.img.copy()

        # Create form frame
        self.form_frame = ttk.Label(self, image=self._background_image)
        self.form_frame.pack(side="bottom", fill="both", expand=True)

        # Bind the frame and the function to resize background
        self.form_frame.bind('<Configure>',self._resize_background)

        # Create username label and entry
        self._username_entry = ttk.Entry(self.form_frame, width=35, font=('Helvetica', 11, 'normal'))
        self._username_entry.insert(0, 'Username')
        self._username_entry.bind('<FocusIn>', self._clear_username)
        self._username_entry.bind('<FocusOut>', self._fill_username)
        self._username_entry.place(relx=0.51, rely=0.55, anchor='center')
        self._username_entry.focus()

        # Create password label and entry
        self._password_entry = ttk.Entry(self.form_frame, width=35, font=('Helvetica', 11, 'normal'))
        self._password_entry.insert(0, 'Password')
        self._password_entry.bind('<FocusIn>', self._clear_password)
        self._password_entry.bind('<FocusOut>', self._fill_password)
        self._password_entry.place(relx=0.51, rely=0.63, anchor='center')

        # remember_me = tk.IntVar()
        # remember_me_check = ttk.Checkbutton(form_frame, text='Remember me', variable=remember_me)
        # remember_me_check.place(relx=0.5, rely=0.7, anchor='center')

        style = ttk.Style()
        style.configure('Custom.TButton', font=('Helvetica', 11, 'normal'))

        # Create login button
        login_button = ttk.Button(self.form_frame, text='Login', width=15, command=self._check_credentials,
                                  style='Custom.TButton', cursor='hand2')
        login_button.place(relx=0.51, rely=0.70, anchor='center')

        # Create forgot password link
        forgot_password_link = ttk.Label(self.form_frame, text='Forgot password?', cursor='hand2',
                                         font=('Helvetica', 10, 'normal', 'underline'))
        forgot_password_link.place(relx=0.51, rely=0.76, anchor='center')
        forgot_password_link.bind("<Button-1>", self.__forgot_password)

    def _resize_background(self, event):

        # Get new height and width from the resize event
        new_height = event.height
        new_width = event.width

        # Resize image based on new dimensions
        self.img = self.img_copy.resize((new_width, new_height))

        # Define new image
        self._background_image = ImageTk.PhotoImage(self.img)

        # Change image in the frame
        self.form_frame.configure(image=self._background_image)

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
        else:
            messagebox.showerror('Login Error', 'Incorrect username or password.')

    @staticmethod
    def __forgot_password(event=None):
        messagebox.showinfo('Forgot Password', 'Please contact the system administrator.')
