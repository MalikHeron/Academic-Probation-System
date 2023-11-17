import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import sv_ttk
from PIL import ImageTk, Image

from database.queries import DatabaseManager
from gui.views import Views
from scripts.gui.report import Report

# setting path
sys.path.append('../../src')


class AcademicProbationSystem:

    def __init__(self):
        self.logo_image = None
        self.background_image = None
        self.window_height = None
        self.window_width = None
        self.splash_window = tk.Tk()
        self.setup_splash_window()
        self.splash_window.after(1000, self.load)
        self.window = None
        DatabaseManager()  # initialize database connection

    def setup_main_window(self):
        # This is where the magic happens
        sv_ttk.set_theme("light")

        # Set window title and icon
        self.window.title('Academic Probation System')
        self.window.iconbitmap('../../res/icon.ico')

        # Set window size
        self.window_width = 1330
        self.window_height = 800

        # Get screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculate position
        position_top = int(screen_height / 2 - self.window_height / 2)
        position_right = int(screen_width / 2 - self.window_width / 2)

        # Set window size and position
        self.window.geometry(f"{self.window_width}x{self.window_height}+{position_right}+{position_top}")
        self.window.resizable(False, False)

        # window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_splash_window(self):
        # Set window size
        self.window_width = 800
        self.window_height = 600

        # Get screen width and height
        screen_width = self.splash_window.winfo_screenwidth()
        screen_height = self.splash_window.winfo_screenheight()

        # Calculate position
        position_top = int(screen_height / 2 - self.window_height / 2)
        position_right = int(screen_width / 2 - self.window_width / 2)

        # Set window size and position
        self.splash_window.geometry(f"{self.window_width}x{self.window_height}+{position_right}+{position_top}")
        self.splash_window.resizable(False, False)

        # Remove window decorations
        self.splash_window.overrideredirect(True)

        # Set window size and position
        self.splash_window.geometry(f"{self.window_width}x{self.window_height}+{position_right}+{position_top}")
        self.splash_window.resizable(False, False)

        # window close event
        self.splash_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create frames
        frame = ttk.Frame(self.splash_window)

        # Place the frames in the window
        frame.grid(row=0, column=0, sticky="nsew")

        # background image
        img = Image.open("../../res/background.png").resize((800, 600))
        self.background_image = ImageTk.PhotoImage(img)  # Keep a reference to the image object

        canvas = tk.Canvas(frame, width=800, height=600)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.background_image, anchor='nw')

        # Create a semi-transparent grey rectangle
        canvas.create_rectangle(0, 0, 800, 600, fill='#808080', stipple='gray25')

        # logo image
        logo_img = Image.open("../../res/logo.png").resize((150, 200))
        self.logo_image = ImageTk.PhotoImage(logo_img)  # Keep a reference to the image object
        canvas.create_image(400, 280, image=self.logo_image)

        # title
        canvas.create_text(400, 400, text="Academic Probation System", font=("Arial", 17, "bold"), fill="white")

    def setup_components(self):
        # Create a style
        style = ttk.Style()

        # Configure the font style for Button
        style.configure('TButton', font=('Helvetica', 10, 'normal'))

        # Configure the font style for Label
        style.configure("TLabel", font=('Helvetica', 11, 'normal'))

        # Configure the font style for Entry (text field)
        style.configure("TEntry", font=('Helvetica', 11, 'normal'))

        # Configure the font style for Treeview (table)
        style.configure("Treeview", font=('Helvetica', 10, 'normal'))

        # Configure the font style for Notebook (tabs)
        style.configure("TNotebook.Tab", font=('Helvetica', 10, 'normal'))

        # Create frames
        frame = ttk.Notebook(self.window)

        # Create tabs
        tab1 = Views(frame).student_view()
        tab2 = Views(frame).module_view()
        tab3 = Views(frame).details_view()
        tab4 = Report(frame).generate_view()

        # Add tabs to notebook
        frame.add(tab1, text='Students')
        frame.add(tab2, text='Modules')
        frame.add(tab3, text='Student Details')
        frame.add(tab4, text='Reports')

        # Place the frames in the window
        frame.pack(fill=tk.BOTH, expand=True)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            DatabaseManager().close_connection()  # close database connection
            self.window.destroy()

    def load(self):
        # Destroy the splash window
        self.splash_window.destroy()

        # Create the main window
        self.window = tk.Tk()

        # Hide the main window
        self.window.withdraw()

        # Set up the main window and its components
        self.setup_main_window()
        self.setup_components()

        # Show the main window and give it focus
        self.window.deiconify()
        self.window.focus_force()

        # Start the main event loop
        self.window.mainloop()

    def run(self):
        self.splash_window.mainloop()


# Create and run the application
app = AcademicProbationSystem()
app.run()
