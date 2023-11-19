import sys
import time
import tkinter as tk
from datetime import datetime
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
        self.emoji_icon = None
        self.greeting_label = None
        self.light_logout_icon = None
        self.dark_logout_icon = None
        self.logout_button = None
        self.start_time = None
        self.time_label = None
        self.dark_theme_icon = None
        self.light_theme_icon = None
        self.theme_button = None
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
        # Set theme
        sv_ttk.set_theme("light")

        # Set window title and icon
        self.window.title('Academic Probation System')
        self.window.iconbitmap('../../res/icon.ico')

        # Set window size
        self.window_width = 1330
        self.window_height = 820

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
        img = Image.open("../../res/splash.jpg").resize((800, 600))
        self.background_image = ImageTk.PhotoImage(img)  # Keep a reference to the image object

        # Create a canvas
        canvas = tk.Canvas(frame, width=800, height=600)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.background_image, anchor='nw')

    def setup_components(self):
        # Set styles
        self.configure_styles()

        # Create a ribbon frame below the tabs
        ribbon_frame = ttk.Frame(self.window)
        ribbon_frame.pack(fill=tk.X)

        # Load the icon and keep it in memory
        self.dark_theme_icon = tk.PhotoImage(file="../../res/switch-light.png")
        self.light_theme_icon = tk.PhotoImage(file="../../res/switch-dark.png")

        # Load the icon and keep it in memory
        self.dark_logout_icon = tk.PhotoImage(file="../../res/logout-light.png")
        self.light_logout_icon = tk.PhotoImage(file="../../res/logout-dark.png")

        # Create a logout button with an icon
        self.logout_button = ttk.Button(ribbon_frame, text="Logout", image=self.dark_logout_icon, compound=tk.LEFT,
                                        takefocus=False, cursor="hand2", command=self.on_closing)
        self.logout_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(5, 5))

        # Create a theme switch button with an icon
        self.theme_button = ttk.Button(ribbon_frame, text="Dark Mode", image=self.dark_theme_icon, compound=tk.LEFT,
                                       command=self.switch_theme, takefocus=False, cursor="hand2")
        self.theme_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(5, 5))

        # Load the icon and keep it in memory
        self.emoji_icon = tk.PhotoImage(file="../../res/smile.png")

        # Create a label to display the time active
        self.greeting_label = ttk.Label(ribbon_frame, text='Welcome back, Malik', image=self.emoji_icon,
                                        compound=tk.RIGHT)
        self.greeting_label.pack(side=tk.LEFT, padx=(10, 0), pady=(5, 5))

        # Create a label to display the time active
        self.time_label = ttk.Label(ribbon_frame, text="")
        self.time_label.pack(side=tk.RIGHT, padx=(0, 20), pady=(5, 5))

        # Record the start time
        self.start_time = time.time()

        # Update the time active every second
        self.update_time()

        # Create frames
        frame = ttk.Notebook(self.window)

        # Create tabs
        tab1 = Views(frame).student_view()
        tab2 = Views(frame).details_view()
        tab3 = Views(frame).staff_view()
        tab4 = Views(frame).module_view()
        tab5 = Views(frame).faculty_view()
        tab6 = Views(frame).school_view()
        tab7 = Views(frame).programme_view()
        tab8 = Report(frame).generate_view()

        # Add tabs to notebook
        frame.add(tab1, text='Students')
        frame.add(tab2, text='Student Details')
        frame.add(tab3, text='Staff')
        frame.add(tab4, text='Modules')
        frame.add(tab5, text='Faculties')
        frame.add(tab6, text='Schools')
        frame.add(tab7, text='Programmes')
        frame.add(tab8, text='Reports')

        # Place the frames in the window
        frame.pack(fill=tk.BOTH, expand=True)

    def on_closing(self):
        if messagebox.askokcancel("Confirm Exit", "Do you want to quit?"):
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

    def update_time(self):
        # Get the current date and time
        now = datetime.now()

        # Format the date and time
        # ("%A, %B %d, %Y %I:%M:%S %p")
        date_time = now.strftime("%I:%M:%S %p")

        # Update the label
        self.time_label.config(text=date_time)

        # Schedule the next update
        self.window.after(100, self.update_time)

    @staticmethod
    def configure_styles():
        # Create a style
        style = ttk.Style()

        # Configure the font style for Button
        style.configure('TButton', font=('Helvetica', 10, 'normal'))

        # Configure the font style for Label
        style.configure('TLabel', font=('Helvetica', 11, 'normal'))

        # Configure the font style for Treeview (table)
        style.configure('Treeview', font=('Helvetica', 10, 'normal'))

        # Configure the font style for Treeview (table) headings
        style.configure('Treeview.Heading', font=("Helvetica", 10, "bold"))

        # Configure the font style for Notebook (tabs)
        style.configure('TNotebook.Tab', focuscolor='', font=('Helvetica', 10, 'normal'))

    def switch_theme(self):
        current_theme = sv_ttk.get_theme()
        if current_theme == "light":
            sv_ttk.set_theme("dark")
            self.theme_button.config(text="Light Mode", image=self.light_theme_icon)
            self.logout_button.config(image=self.light_logout_icon)
            self.configure_styles()
        else:
            sv_ttk.set_theme("light")
            self.theme_button.config(text="Dark Mode", image=self.dark_theme_icon)
            self.logout_button.config(image=self.dark_logout_icon)
            self.configure_styles()

    def run(self):
        self.splash_window.mainloop()


# Create and run the application
app = AcademicProbationSystem()
app.run()
