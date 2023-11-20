import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import sv_ttk

from database.queries import DatabaseManager
from scripts.gui.dashboard import Dashboard
from scripts.gui.login import Login

# setting path
sys.path.append('../../src')


class AcademicProbationSystem(tk.Tk):

    def __init__(self):
        super().__init__()

        # Hide the window
        self.withdraw()

        # Set window title and icon
        self.title('Academic Probation System')
        self.iconbitmap('../../res/icon.ico')

        # Set window size
        self.window_width = 1330
        self.window_height = 820

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position
        position_top = int(screen_height / 2 - self.window_height / 2)
        position_right = int(screen_width / 2 - self.window_width / 2)

        # Set window size and position
        self.geometry(f"{self.window_width}x{self.window_height}+{position_right}+{position_top}")
        self.resizable(False, False)

        # window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize frames
        self.frames = {}

        # Set theme
        sv_ttk.set_theme("light")

        # Create LoginFrame and add it to frames dictionary
        login_frame = Login(master=self)
        self.frames['login'] = login_frame
        login_frame.grid(row=0, column=0, sticky="nsew")

        # Create MainFrame and add it to frames dictionary
        main_frame = Dashboard(master=self)
        self.frames['main'] = main_frame
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Raise the login frame
        self.raise_frame('login')

        # Show the window
        self.deiconify()

    def on_closing(self):
        if messagebox.askokcancel("Confirm Exit", "Do you want to quit?"):
            DatabaseManager().close_connection()  # close database connection
            self.destroy()

    def raise_frame(self, name, user=None):
        # Destroy the current frame
        for frame in self.frames.values():
            frame.destroy()

        # Create a new frame and add it to frames dictionary
        if name == 'login':
            self.frame = Login(master=self)
        elif name == 'dashboard':
            self.frame = Dashboard(user=user, master=self)

        self.frames[name] = self.frame
        self.frame.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def configure_styles():
        # Create a style
        style = ttk.Style()

        # Configure the font style for Button
        style.configure('TButton', font=('Helvetica', 10, 'normal'))

        # Configure the font style for TCheckbutton
        style = ttk.Style()
        style.configure('TCheckbutton', font=('Helvetica', 10, 'normal'))

        # Configure the font style for Label
        style.configure('TLabel', font=('Helvetica', 11, 'normal'))

        # Configure the font style for Treeview (table)
        style.configure('Treeview', font=('Helvetica', 10, 'normal'))

        # Configure the font style for Treeview (table) headings
        style.configure('Treeview.Heading', font=("Helvetica", 10, "bold"))

        # Configure the font style for Notebook (tabs)
        style.configure('TNotebook.Tab', focuscolor='', font=('Helvetica', 10, 'normal'))

    def run(self):
        self.mainloop()


# Create and run the application
app = AcademicProbationSystem()
app.run()
