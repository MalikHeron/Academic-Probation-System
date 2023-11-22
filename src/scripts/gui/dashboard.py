import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk

import sv_ttk

from scripts.gui.report import Report
from scripts.gui.views import Views


class Dashboard(tk.Frame):
    def __init__(self, user=None, master=None):
        super().__init__(master)
        # Set styles
        self.master.configure_styles()

        # Create a style
        sv_ttk.use_light_theme()

        # Create a ribbon frame below the tabs
        ribbon_frame = ttk.Frame(self)
        ribbon_frame.pack(fill=tk.X)

        # Load the icon and keep it in memory
        self._dark_theme_icon = tk.PhotoImage(file="../../res/switch-light.png")
        self._light_theme_icon = tk.PhotoImage(file="../../res/switch-dark.png")

        # Load the icon and keep it in memory
        self._dark_logout_icon = tk.PhotoImage(file="../../res/logout-light.png")
        self._light_logout_icon = tk.PhotoImage(file="../../res/logout-dark.png")

        # Create a logout button with an icon
        self._logout_button = ttk.Button(ribbon_frame, text="Logout", image=self._dark_logout_icon, compound=tk.LEFT,
                                         takefocus=False, cursor="hand2", command=self._logout)
        self._logout_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(5, 5))

        # Create a theme switch button with an icon
        self._theme_button = ttk.Button(ribbon_frame, text="Dark Mode", image=self._dark_theme_icon, compound=tk.LEFT,
                                        command=self.switch_theme, takefocus=False, cursor="hand2")
        self._theme_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(5, 5))

        # Load the icons and keep them in memory
        self._emoji_icons = {
            "morning": tk.PhotoImage(file="../../res/smile_teeth.png"),
            "afternoon": tk.PhotoImage(file="../../res/smile.png"),
            "evening": tk.PhotoImage(file="../../res/sunglass.png"),
            "night": tk.PhotoImage(file="../../res/sleep.png"),
            "late_night": tk.PhotoImage(file="../../res/cry.png"),
        }

        # Create a label to display the time active
        self._greeting_label = ttk.Label(ribbon_frame, text=f'Welcome back, {user}', image=self._emoji_icons["morning"],
                                         compound=tk.RIGHT)
        self._greeting_label.pack(side=tk.LEFT, padx=(10, 0), pady=(5, 5))

        # Create a label to display the time active
        self._time_label = ttk.Label(ribbon_frame, text="")
        self._time_label.pack(side=tk.RIGHT, padx=(0, 20), pady=(5, 5))

        # Record the start time
        self._start_time = time.time()

        # Update the time active every second
        self._update_time()

        # Create frames
        frame = ttk.Notebook(self)

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

    def _logout(self):
        if messagebox.askokcancel("Confirm Logout", "Do you want to logout?"):
            # Switch back to the login frame
            self.master.raise_frame('login')

    def _update_time(self):
        # Get the current date and time
        now = datetime.now()
        hour = now.hour

        if 5 <= hour < 12:
            emoji = self._emoji_icons["morning"]
        elif 12 <= hour < 17:
            emoji = self._emoji_icons["afternoon"]
        elif 17 <= hour < 21:
            emoji = self._emoji_icons["evening"]
        elif 21 <= hour < 24:
            emoji = self._emoji_icons["night"]
        else:  # from midnight to 5am
            emoji = self._emoji_icons["late_night"]

        # Update the label
        self._greeting_label.config(image=emoji)

        # Format the date and time
        date_time = now.strftime("%I:%M:%S %p")

        # Update the label
        self._time_label.config(text=date_time)

        # Schedule the next update
        self.after(100, self._update_time)

    def switch_theme(self):
        current_theme = sv_ttk.get_theme()
        if current_theme == "light":
            sv_ttk.set_theme("dark")
            self._theme_button.config(text="Light Mode", image=self._light_theme_icon)
            self._logout_button.config(image=self._light_logout_icon)
        else:
            sv_ttk.set_theme("light")
            self._theme_button.config(text="Dark Mode", image=self._dark_theme_icon)
            self._logout_button.config(image=self._dark_logout_icon)
