import configparser
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk

import darkdetect
import sv_ttk

from scripts.gui.dialogs import Dialog
from scripts.gui.report import Report
from scripts.gui.views import Views


class Dashboard(tk.Frame):
    def __init__(self, user=None, master=None):
        super().__init__(master)
        # Load the configuration
        self._config = configparser.ConfigParser()
        self._config.read('../../config/config.ini')

        # Set styles
        self.configure_styles()

        # Create a ribbon frame below the tabs
        ribbon_frame = ttk.Frame(self)
        ribbon_frame.pack(fill=tk.X)

        # Load the icon and keep it in memory
        self._dark_theme_icon = tk.PhotoImage(file="../../res/switch-light.png")
        self._light_theme_icon = tk.PhotoImage(file="../../res/switch-dark.png")

        # Load the icon and keep it in memory
        self._dark_logout_icon = tk.PhotoImage(file="../../res/logout-dark.png")
        self._light_logout_icon = tk.PhotoImage(file="../../res/logout-light.png")

        # Load the icon and keep it in memory
        self._dark_settings_icon = tk.PhotoImage(file="../../res/settings-dark.png")
        self._light_settings_icon = tk.PhotoImage(file="../../res/settings-light.png")

        # Create a logout button with an icon
        self._logout_button = ttk.Button(ribbon_frame, text="Logout", image=self._light_logout_icon, compound=tk.LEFT,
                                         takefocus=False, cursor="hand2", command=self._logout)
        self._logout_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(5, 5))

        # Create a theme switch button with an icon
        self._settings_button = ttk.Button(ribbon_frame, text="Settings", image=self._light_settings_icon,
                                           compound=tk.LEFT,
                                           command=self._open_settings, takefocus=False, cursor="hand2")
        self._settings_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(5, 5))

        # Create a theme switch button with an icon
        self._theme_button = ttk.Button(ribbon_frame, text="Dark Mode", image=self._dark_theme_icon, compound=tk.LEFT,
                                        command=self.switch_theme, takefocus=False, cursor="hand2")
        self._theme_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(5, 5))

        # Check the theme
        self.set_theme()

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

    def _open_settings(self):
        _dialog = Dialog(self)
        _dialog.settings_dialog(self._config)
        _dialog.wait_window()
        if _dialog.theme is not None:
            # Save the theme to the config file
            self.set_theme_config(_dialog.theme)

            if _dialog.theme == 'auto':
                self.update_theme(darkdetect.isDark())
        # Set styles
        self.configure_styles()

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

    def set_theme(self):
        # Set styles
        self.configure_styles()
        # Check if the theme is set in the config file
        if self._config.has_section('Theme') and self._config.has_option('Theme', 'theme'):
            theme = self._config.get('Theme', 'theme')
            if theme == 'auto':
                if darkdetect.isDark():
                    self.set_dark_theme()
                else:
                    self.set_light_theme()
                self.update_theme(darkdetect.isDark())
            elif theme == 'dark':
                self.set_dark_theme()
            else:
                self.set_light_theme()
        else:
            # Create a style
            sv_ttk.use_light_theme()
            self.configure_styles()

    def update_theme(self, is_dark):
        # Check if the theme is set in the config file
        if self._config.has_section('Theme') and self._config.has_option('Theme', 'theme'):
            theme = self._config.get('Theme', 'theme')
            if theme == 'auto':
                current_theme = sv_ttk.get_theme()
                if is_dark and current_theme != 'dark':
                    self.set_dark_theme()
                elif not is_dark and current_theme != 'light':
                    self.set_light_theme()
            # Schedule the next update
            self.after(1000, self.update_theme, darkdetect.isDark())

    def set_dark_theme(self):
        self._theme_button.config(text="Light Mode", image=self._light_theme_icon)
        self._logout_button.config(image=self._dark_logout_icon)
        self._settings_button.config(image=self._dark_settings_icon)
        sv_ttk.use_dark_theme()
        self.configure_styles()

    def set_light_theme(self):
        self._theme_button.config(text="Dark Mode", image=self._dark_theme_icon)
        self._logout_button.config(image=self._light_logout_icon)
        self._settings_button.config(image=self._light_settings_icon)
        sv_ttk.use_light_theme()
        self.configure_styles()

    def switch_theme(self):
        # Get the current theme
        current_theme = sv_ttk.get_theme()
        if current_theme == "light":
            self.set_theme_config("dark")
            self.set_dark_theme()
        else:
            self.set_theme_config("light")
            self.set_light_theme()

    def set_theme_config(self, theme):
        # Save the theme to the config file
        self._config['Theme'] = {'theme': theme}
        with open('../../config/config.ini', 'w') as configfile:
            self._config.write(configfile)

    def configure_styles(self):
        # Create a style
        style = ttk.Style()

        # Define default font settings
        default_font_settings = {
            'button_family': 'Helvetica',
            'button_size': '10',
            'button_style': 'normal',
            'label_family': 'Helvetica',
            'label_size': '11',
            'label_style': 'normal',
            'tree_family': 'Helvetica',
            'tree_size': '10',
            'tree_style': 'normal',
            'heading_family': 'Helvetica',
            'heading_size': '10',
            'heading_style': 'bold',
            'tab_family': 'Helvetica',
            'tab_size': '10',
            'tab_style': 'normal'
        }

        # Get the font settings from the config file or use default values
        # We use a dictionary comprehension to iterate over each setting in default_font_settings
        # For each setting, we check if it exists in the config file
        # If it does, we get its value from the config file
        # If it doesn't, we use the default value from default_font_settings
        font_settings = {
            setting: self._config.get('Font', setting) if self._config.has_option('Font', setting) else
            default_font_settings[
                setting]
            for setting in default_font_settings
        }

        # Configure the font styles
        # For each widget type, we get the font family, size, and style from font_settings
        # We then use these values to configure the style for that widget type
        style.configure('TButton', font=(
            font_settings['button_family'], font_settings['button_size'], font_settings['button_style']))
        style.configure('TCheckbutton', font=('Helvetica', 10, 'normal'))
        style.configure('TLabel',
                        font=(font_settings['label_family'], font_settings['label_size'], font_settings['label_style']))
        style.configure('Treeview', font=(
            font_settings['tree_family'], font_settings['tree_size'], font_settings['tree_style']))
        style.configure('Treeview.Heading', font=(
            font_settings['heading_family'], font_settings['heading_size'], font_settings['heading_style']))
        style.configure('TNotebook.Tab', focuscolor='',
                        font=(font_settings['tab_family'], font_settings['tab_size'], font_settings['tab_style']))
