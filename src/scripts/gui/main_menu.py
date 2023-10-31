import tkinter as tk

class MainMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setup_components()

    def setup_components(self):
        # buttons
        self.button1 = tk.Button(self, text="View Students", command=self.view_students)
        self.button1.pack(fill=tk.BOTH, expand=True)

        self.button2 = tk.Button(self, text="Add Student", command=self.add_student)
        self.button2.pack(fill=tk.BOTH, expand=True)

        self.button3 = tk.Button(self, text="Remove Student", command=self.remove_student)
        self.button3.pack(fill=tk.BOTH, expand=True)

    
    def view_students(self):
        print("View Students")

    def add_student(self):
        print("Add Student")

    def remove_student(self):
        print("Remove Student")