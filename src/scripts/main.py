import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from PIL import ImageTk, Image

from database.queries import DatabaseManager
from gui.main_menu import MainMenu

# setting path
sys.path.append('../../src')


class AcademicProbationSystem:

    def __init__(self):
        self.logo_image = None
        self.background_image = None
        self.window_height = None
        self.window_width = None
        self.window = tk.Tk()
        self.window.title('Academic Probation System')
        self.setup_window()
        self.setup_components()
        DatabaseManager()  # initialize database connection

    def setup_window(self):
        # Set window size
        self.window_width = 1300
        self.window_height = 600

        # Get screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculate position
        position_top = int(screen_height / 2 - self.window_height / 2)
        position_right = int(screen_width / 2 - self.window_width / 2)

        # Set window size and position
        self.window.geometry(f"{self.window_width}x{self.window_height}+{position_right}+{position_top}")
        self.window.resizable(False, False)

        # Make the columns equal width
        self.window.columnconfigure(0, weight=1, minsize=650)
        self.window.columnconfigure(1, weight=1, minsize=650)

        # window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            DatabaseManager().close_connection()  # close database connection
            self.window.destroy()

    def setup_components(self):
        frame1 = ttk.Frame(self.window)
        frame2 = MainMenu(self.window)

        # Place the frames in the window
        frame1.grid(row=0, column=0, sticky="nsew")
        frame2.grid(row=0, column=1, sticky="ew")

        # background image
        img = Image.open("../../res/background.png").resize((650, 600))
        self.background_image = ImageTk.PhotoImage(img)  # Keep a reference to the image object

        canvas = tk.Canvas(frame1, width=650, height=600)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.background_image, anchor='nw')

        # Create a semi-transparent grey rectangle
        canvas.create_rectangle(0, 0, 650, 600, fill='#808080', stipple='gray25')

        logo_img = Image.open("../../res/logo.png").resize((150, 200))
        self.logo_image = ImageTk.PhotoImage(logo_img)  # Keep a reference to the image object
        canvas.create_image(325, 240, image=self.logo_image)

        canvas.create_text(325, 360, text="Academic Probation System", font=("Arial", 17, "bold"), fill="white")

        frame2.grid(row=0, column=1, sticky="ew")

    def run(self):
        self.window.mainloop()


# Create and run the application
app = AcademicProbationSystem()
app.run()
