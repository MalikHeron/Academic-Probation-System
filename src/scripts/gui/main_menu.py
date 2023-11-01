import tkinter as tk
from tkinter import ttk

from src.scripts.prolog_interface import PrologQueryHandler


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

    def sort_column(self, tree, col, reverse):
        column_data = [(tree.set(child_id, col), child_id) for child_id in tree.get_children('')]
        column_data.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, child_id) in enumerate(column_data):
            tree.move(child_id, '', index)

        # reverse sort next time column is clicked
        tree.heading(col, command=lambda: self.sort_column(tree, col, not reverse))

    def view_students(self):
        # Create student frame
        self.student_frame = tk.Frame(self.parent)
        self.student_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Create a style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        # Labels
        tk.Label(self.student_frame, text="University of Technology", font=("Helvetica", 10, "bold")).pack()
        tk.Label(self.student_frame, text="Academic Probation Alert System").pack()
        tk.Label(self.student_frame, text="Academic Affairs").pack()
        tk.Label(self.student_frame, text="Student Listing").pack()

        # Create Canvas in new window
        canvas = tk.Canvas(self.student_frame)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)

        # Add a Scrollbar to the Canvas
        scrollbar = ttk.Scrollbar(self.student_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create another frame inside the canvas
        second_frame = tk.Frame(canvas)
        second_frame.pack(fill='both', expand=True)

        # Add that new frame to a new window on the canvas
        canvas.create_window((0, 0), window=second_frame, anchor="nw")

        # Create Treeview in second frame
        tree = ttk.Treeview(second_frame, show='headings', style="Treeview")

        # Define columns
        columns = ("Student ID", "Student Name", "Student Email", "School", "Programme")
        tree["columns"] = columns

        # Format columns
        for col in columns:
            tree.column(col, width=len(col) * 16)
            tree.heading(col, text=col, command=lambda _col=col: self.sort_column(tree, _col, False))

        # Insert data in table
        for student in PrologQueryHandler.get_student_list():
            student_id, name, email, school, programme = student.values()
            tree.insert("", "end", values=(student_id, name, email, school, programme))

        tree.pack()
        close_button = tk.Button(self.student_frame, text="Close", command=self.close_student_view)

        # Center the close button at the bottom of the window
        close_button.place(relx=0.5, rely=0.97, anchor='s')


    def add_student(self):
        print("Add Student")


    def remove_student(self):
        print("Remove Student")

    def add_details(self):
        print("Add Details")

    def close_student_view(self):
        # Hide student frame and show main frame
        self.student_frame.grid_forget()
