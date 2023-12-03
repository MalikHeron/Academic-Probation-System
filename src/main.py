import json
import tkinter as tk
from tkinter import messagebox

from gui.dashboard import Dashboard
from gui.login import Login


class AcademicProbationSystem(tk.Tk):

    def __init__(self):
        super().__init__()

        # Hide the window
        self.withdraw()

        # Load the configuration
        self._config = self.load_config()

        # Set window title and icon
        self.title('Academic Probation System')
        self.iconbitmap('res/icon.ico')

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set window size to 80% of the screen size
        self.window_width = int(screen_width * 0.8)
        self.window_height = int(screen_height * 0.8)

        # Calculate position
        position_top = int(screen_height / 2 - self.window_height / 2)
        position_right = int(screen_width / 2 - self.window_width / 2)

        # Set window size and position
        self.geometry(f"{self.window_width}x{self.window_height}+{position_right}+{position_top}")
        self.resizable(True, True)

        # Set minimum window size
        self.minsize(1280, 768)

        # window close events
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Initialize frames
        self._frames = {}

        # Fill the entire window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Raise the login frame
        self.raise_frame('login')

        # Check if the window was maximized last time
        if self._config.get('DEFAULT', {}).get('Maximized', False):
            self.state('zoomed')

        # Show the window
        self.deiconify()

    @staticmethod
    def load_config():
        try:
            with open('../config/window_state.json', 'r') as configfile:
                return json.load(configfile)
        except FileNotFoundError:
            return {}

    def _on_closing(self):
        self._config['DEFAULT'] = {'Maximized': self.state() == 'zoomed'}
        with open('../config/window_state.json', 'w') as configfile:
            json.dump(self._config, configfile)

        # Ask the user if they want to quit
        if messagebox.askokcancel("Confirm Exit", "Do you want to quit?"):
            self.destroy()

    def raise_frame(self, name, user=None):
        # Destroy the current frame
        for frame in self._frames.values():
            frame.destroy()

        # Create a new frame and add it to frames dictionary
        if name == 'login':
            self.frame = Login(master=self)
        elif name == 'dashboard':
            self.frame = Dashboard(user=user, master=self)

        self._frames[name] = self.frame
        self.frame.grid(row=0, column=0, sticky="nsew")

    def run(self):
        self.mainloop()


# Create and run the application
app = AcademicProbationSystem()
app.run()
