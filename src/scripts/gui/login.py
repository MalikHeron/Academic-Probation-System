import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title('Login Screen')

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack()

        self.username_label = ttk.Label(self.login_frame, text='Username:')
        self.username_label.grid(row=0, column=0)

        self.username_entry = ttk.Entry(self.login_frame, textvariable=self.username)
        self.username_entry.grid(row=0, column=1)

        self.password_label = ttk.Label(self.login_frame, text='Password:')
        self.password_label.grid(row=1, column=0)

        self.password_entry = ttk.Entry(self.login_frame, textvariable=self.password, show='*')
        self.password_entry.grid(row=1, column=1)

        self.login_button = ttk.Button(self.login_frame, text='Login', command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2)

    def login(self):
        username = self.username.get()
        password = self.password.get()

        # Add your own authentication logic here
        if username == 'admin' and password == 'password':
            messagebox.showinfo('Login info', 'Welcome Admin!')
        else:
            messagebox.showerror('Login error', 'Incorrect username or password')


root = tk.Tk()
login_screen = LoginScreen(root)
root.mainloop()
