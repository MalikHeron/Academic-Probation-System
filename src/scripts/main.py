import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from PIL import ImageTk, Image

from gui.main_menu import MainMenu
from scripts.database.queries import DatabaseManager

# setting path
sys.path.append('../../src')


class AcademicProbationSystem:

    def __init__(self):
        self.window_height = None
        self.window_width = None
        self.window = tk.Tk()
        self.window.title('Academic Probation System')
        self.setup_window()
        self.setup_components()
        DatabaseManager()  # initialize database connection

    def setup_window(self):
        # Set window size
        self.window_width = 1000
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
        self.window.columnconfigure(0, weight=1, minsize=500)
        self.window.columnconfigure(1, weight=1, minsize=500)

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
        img = Image.open("../../res/background.png").resize((500, 600))
        background_image = ImageTk.PhotoImage(img)

        background = tk.Label(frame1, image=background_image, width=500, height=600)
        background.image = background_image
        background.pack(fill=tk.BOTH, expand=True)

        content = tk.Frame(background, background='', width=500, height=600)
        content.place(x=0, y=0, width=500, height=600)

        logo_image = ImageTk.PhotoImage(Image.open("../../res/logo.png").resize((150, 200)))
        logo_label = ttk.Label(content, image=logo_image, background="")
        logo_label.image = logo_image
        logo_label.place(relx=0.5, rely=0.4, anchor='center')  # Centered horizontally and placed at 40% of the height

        label1 = ttk.Label(content, text="Academic Probation System", font=("Arial", 17, "bold"), background="")
        label1.place(relx=0.5, rely=0.6, anchor='center')  # Centered both horizontally and vertically

    def run(self):
        self.window.mainloop()


# Create and run the application
app = AcademicProbationSystem()
app.run()
