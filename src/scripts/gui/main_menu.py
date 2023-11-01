import tkinter as tk
from tkinter import ttk

from src.scripts.prolog_interface import PrologQueryHandler


def sort_column(tree, col, reverse):
    column_data = [(tree.set(child_id, col), child_id) for child_id in tree.get_children('')]
    column_data.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, child_id) in enumerate(column_data):
        tree.move(child_id, '', index)

    # reverse sort next time column is clicked
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))


class MainMenu(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.student_frame = None
        self.view_modules_button = None
        self.add_student_button = None
        self.view_students_button = None
        self.title = None
        self.parent = parent

        self.setup_components()

    def setup_components(self):
        # title
        self.title = tk.Label(self, text="Main Menu", font=('Arial', 16, 'bold'))
        self.title.configure(foreground='black')
        self.title.pack(padx=20, pady=20, fill='x', expand=True)

        # buttons
        self.view_students_button = tk.Button(self, text="View Students", command=self.view_students)
        self.view_students_button.configure(background='#02d971', foreground='#ffffff', font=('Arial', 12, 'bold'),
                                            relief='groove')
        self.view_students_button.pack(padx=40, pady=5, fill='x', expand=True)

        self.add_student_button = tk.Button(self, text="Add Student", command=self.add_student)
        self.add_student_button.configure(background='#02d971', foreground='#ffffff', font=('Arial', 12, 'bold'),
                                          relief='groove')
        self.add_student_button.pack(padx=40, pady=5, fill='x', expand=True)

        self.view_modules_button = tk.Button(self, text="View Modules", command=self.view_modules)
        self.view_modules_button.configure(background='#02d971', foreground='#ffffff', font=('Arial', 12, 'bold'),
                                           relief='groove')
        self.view_modules_button.pack(padx=40, pady=5, fill='x', expand=True)

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

        # Create another frame inside the canvas
        second_frame = tk.Frame(canvas)

        # Add that new frame to a new window on the canvas
        canvas.create_window((0, 0), window=second_frame, anchor="nw")

        def on_configure(event):
            # Update scroll region after starting 'mainloop'
            # When all widgets are in canvas
            canvas.configure(scrollregion=canvas.bbox('all'))

            # Set second frame's size to canvas's size
            second_frame.configure(width=event.width)

        canvas.bind('<Configure>', on_configure)

        # Create Treeview in second frame
        tree = ttk.Treeview(second_frame, show='headings', style="Treeview", height=20)

        # Add a Scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(second_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        # Configure the Treeview
        tree.configure(yscrollcommand=scrollbar.set)

        # Define columns
        columns = ("Student ID", "Student Name", "Student Email", "School", "Programme")
        tree["columns"] = columns

        # Format columns
        column_widths = [100, 150, 250, 250, 200]  # Adjust these values as needed
        for col, width in zip(columns, column_widths):
            tree.column(col, width=width)
            tree.heading(col, text=col, command=lambda _col=col: sort_column(tree, _col, False))

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

    def view_modules(self):
        print("View Modules")

    def add_details(self):
        print("Add Details")

    def close_student_view(self):
        # Hide student frame and show main frame
        self.student_frame.grid_forget()
