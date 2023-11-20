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
        login_frame = LoginFrame(master=self)
        self.frames['login'] = login_frame
        login_frame.grid(row=0, column=0, sticky="nsew")

        # Create MainFrame and add it to frames dictionary
        main_frame = MainFrame(master=self)
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
            self.frame = LoginFrame(master=self)
        elif name == 'main':
            self.frame = MainFrame(user=user, master=self)

        self.frames[name] = self.frame
        self.frame.grid(row=0, column=0, sticky="nsew")

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

    def run(self):
        self.mainloop()


class LoginFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # Set styles
        self.master.configure_styles()

        # Set theme
        sv_ttk.use_dark_theme()

        # background image
        img = Image.open("../../res/login-background.png").resize((1350, 850))
        self.background_image = ImageTk.PhotoImage(img)  # Keep a reference to the image object
        form_frame = ttk.Label(self, image=self.background_image)
        form_frame.pack(side="bottom", fill="both", expand=True)

        self.username_entry = ttk.Entry(form_frame, width=35, font=('Helvetica', 11, 'normal'))
        self.username_entry.insert(0, 'Username')
        self.username_entry.bind('<FocusIn>', self.clear_username)
        self.username_entry.bind('<FocusOut>', self.fill_username)
        self.username_entry.place(relx=0.51, rely=0.55, anchor='center')

        self.password_entry = ttk.Entry(form_frame, width=35, font=('Helvetica', 11, 'normal'))
        self.password_entry.insert(0, 'Password')
        self.password_entry.bind('<FocusIn>', self.clear_password)
        self.password_entry.bind('<FocusOut>', self.fill_password)
        self.password_entry.place(relx=0.51, rely=0.65, anchor='center')

        #  remember_me = tk.IntVar()
        #  remember_me_check = ttk.Checkbutton(form_frame, text='Remember me', variable=remember_me)
        #  remember_me_check.place(relx=0.5, rely=0.6, anchor='center')

        style = ttk.Style()
        style.configure('Custom.TButton', font=('Helvetica', 11, 'normal'))

        submit_button = ttk.Button(form_frame, text='Login', command=self.check_credentials, style='Custom.TButton')
        submit_button.place(relx=0.51, rely=0.75, anchor='center')

        #  forgot_password_link = ttk.Button(form_frame, text='Forgot password?', command=self.forgot_password)
        #  forgot_password_link.place(relx=0.5, rely=0.8, anchor='center')

    def clear_username(self, event):
        if self.username_entry.get() == 'Username':
            self.username_entry.delete(0, tk.END)

    def fill_username(self, event):
        if self.username_entry.get() == '':
            self.username_entry.insert(0, 'Username')

    def clear_password(self, event):
        if self.password_entry.get() == 'Password':
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(show='*')

    def fill_password(self, event):
        if self.password_entry.get() == '':
            self.password_entry.insert(0, 'Password')
            self.password_entry.config(show='')

    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = DatabaseManager().get_credentials(username, password)

        # Check if username and password are correct
        if user_id:
            user = DatabaseManager().get_staff_name(user_id)
            self.master.raise_frame('main', user)
        else:
            messagebox.showerror('Login error', 'Incorrect username or password')

    @staticmethod
    def forgot_password():
        messagebox.showinfo('Forgot Password', 'Please contact the system administrator.')


class MainFrame(tk.Frame):
    def __init__(self, user=None, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # Set styles
        self.master.configure_styles()

        # Create a style
        sv_ttk.use_light_theme()

        # Create a ribbon frame below the tabs
        ribbon_frame = ttk.Frame(self)
        ribbon_frame.pack(fill=tk.X)

        # Load the icon and keep it in memory
        self.dark_theme_icon = tk.PhotoImage(file="../../res/switch-light.png")
        self.light_theme_icon = tk.PhotoImage(file="../../res/switch-dark.png")

        # Load the icon and keep it in memory
        self.dark_logout_icon = tk.PhotoImage(file="../../res/logout-light.png")
        self.light_logout_icon = tk.PhotoImage(file="../../res/logout-dark.png")

        # Create a logout button with an icon
        self.logout_button = ttk.Button(ribbon_frame, text="Logout", image=self.dark_logout_icon, compound=tk.LEFT,
                                        takefocus=False, cursor="hand2", command=self.logout)
        self.logout_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(5, 5))

        # Create a theme switch button with an icon
        self.theme_button = ttk.Button(ribbon_frame, text="Dark Mode", image=self.dark_theme_icon, compound=tk.LEFT,
                                       command=self.switch_theme, takefocus=False, cursor="hand2")
        self.theme_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(5, 5))

        # Load the icon and keep it in memory
        self.emoji_icon = tk.PhotoImage(file="../../res/smile.png")

        # Create a label to display the time active
        self.greeting_label = ttk.Label(ribbon_frame, text=f'Welcome back, {user}', image=self.emoji_icon,
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

    def logout(self):
        if messagebox.askokcancel("Confirm Logout", "Do you want to logout?"):
            # Switch back to the login frame
            self.master.raise_frame('login')

    def update_time(self):
        # Get the current date and time
        now = datetime.now()

        # Format the date and time
        date_time = now.strftime("%I:%M:%S %p")

        # Update the label
        self.time_label.config(text=date_time)

        # Schedule the next update
        self.after(100, self.update_time)

    def switch_theme(self):
        current_theme = sv_ttk.get_theme()
        if current_theme == "light":
            sv_ttk.set_theme("dark")
            self.theme_button.config(text="Light Mode", image=self.light_theme_icon)
            self.logout_button.config(image=self.light_logout_icon)
        else:
            sv_ttk.set_theme("light")
            self.theme_button.config(text="Dark Mode", image=self.dark_theme_icon)
            self.logout_button.config(image=self.dark_logout_icon)


# Create and run the application
app = AcademicProbationSystem()
app.run()
