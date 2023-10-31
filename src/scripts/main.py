import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from database import DatabaseManager
from prolog_interface import PrologQueryHandler as Prolog
from gui.main_menu import MainMenu


def create_directory():
    if not os.path.exists("../../logs"):
        os.makedirs("../../logs")
    if not os.path.exists("../../data"):
        os.makedirs("../../data")


class AcademicProbationSystem:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Academic Probation System')
        self.setup_window()
        self.setup_components()
        create_directory()
        DatabaseManager()

    def setup_window(self):
        # Set window size
        self.window_width = 800
        self.window_height = 400

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
        self.window.columnconfigure(0, weight=1, minsize=400)
        self.window.columnconfigure(1, weight=1, minsize=400)

    def setup_components(self):
        frame1 = ttk.Frame(self.window)
        frame2 = MainMenu(self.window)

        # Place the frames in the window
        frame1.grid(row=0, column=0, sticky="nsew")
        frame2.grid(row=0, column=1, sticky="nsew")

        # background image
        img = Image.open("../assets/background.png").resize((400, 400))
        background_image = ImageTk.PhotoImage(img)

        background = tk.Label(frame1, image=background_image, width=400, height=400)
        background.image = background_image
        background.pack(fill=tk.BOTH, expand=True)

        content = tk.Frame(background, background='', width=400, height=400)
        content.place(x=0, y=0, width=400, height=400)

        logo_image = ImageTk.PhotoImage(Image.open("../assets/utech-logo.png").resize((150, 200)))
        logo_label = ttk.Label(content, image=logo_image, background="")
        logo_label.image = logo_image
        logo_label.pack(pady=20)

        label1 = ttk.Label(content, text="Academic Probation System", font=("Arial", 17, "bold"), background="")
        label1.pack()

    def run(self):
        self.window.mainloop()


# Create and run the application
app = AcademicProbationSystem()
app.run()
