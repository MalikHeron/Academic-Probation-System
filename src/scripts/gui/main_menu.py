import tkinter as tk

class MainMenu(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setup_components()

    def setup_components(self):
        # title
        self.title = tk.Label(self, text="Main Menu", font=('Arial', 16, 'bold'))
        self.title.configure(foreground='black')
        self.title.pack(padx=20, pady=20, fill='x', expand=True)

        # buttons
        self.button1 = tk.Button(self, text="View Students", command=self.view_students)
        self.button1.configure(background='#02d971', foreground='#ffffff', font=('Arial', 12, 'bold'), relief='groove')
        self.button1.pack(padx=40, pady=5, fill='x', expand=True)

        self.button2 = tk.Button(self, text="Add Student", command=self.add_student)
        self.button2.configure(background='#02d971', foreground='#ffffff', font=('Arial', 12, 'bold'), relief='groove')
        self.button2.pack(padx=40, pady=5, fill='x', expand=True)

        self.button3 = tk.Button(self, text="Remove Student", command=self.remove_student)
        self.button3.configure(background='#02d971', foreground='#ffffff', font=('Arial', 12, 'bold'), relief='groove')
        self.button3.pack(padx=40, pady=5, fill='x', expand=True)

    
    def view_students(self):
        print("View Students")

    def add_student(self):
        print("Add Student")

    def remove_student(self):
        print("Remove Student")