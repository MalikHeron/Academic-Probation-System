import tkinter as tk
from tkinter import ttk, simpledialog

from scripts.gui.generate_report import GenerateReportFrame
from src.scripts.database import DatabaseManager

db_manager = DatabaseManager()  # create an instance of DatabaseManager


def sort_column(tree, col, reverse):
    column_data = [(tree.set(child_id, col), child_id) for child_id in tree.get_children('')]
    column_data.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, child_id) in enumerate(column_data):
        tree.move(child_id, '', index)

    # reverse sort next time column is clicked
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))


def generate_report():
    GenerateReportFrame(tk.Tk(), "Generate Report")


class MainMenu(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.generate_report_button = None
        self.add_details_button = None
        self.student_frame = None
        self.module_frame = None
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

        # student buttons
        self.view_students_button = tk.Button(self, text="View Students", command=self.view_students)
        self.view_students_button.configure(background='#61CBEC', foreground='#000000', font=('Arial', 12, 'normal'),
                                            relief='groove')
        self.view_students_button.pack(padx=40, pady=5, fill='x', expand=True)

        # module buttons
        self.view_modules_button = tk.Button(self, text="View Modules", command=self.view_modules)
        self.view_modules_button.configure(background='#61CBEC', foreground='#000000', font=('Arial', 12, 'normal'),
                                           relief='groove')
        self.view_modules_button.pack(padx=40, pady=5, fill='x', expand=True)

        # details button
        self.add_details_button = tk.Button(self, text="View Details", command=self.add_details)
        self.add_details_button.configure(background='#61CBEC', foreground='#000000', font=('Arial', 12, 'normal'),
                                          relief='groove')
        self.add_details_button.pack(padx=40, pady=5, fill='x', expand=True)

        # generate report button
        self.generate_report_button = tk.Button(self, text="Generate Report", command=generate_report)
        self.generate_report_button.configure(background='#936BE9', foreground='#000000', font=('Arial', 12, 'normal'),
                                              relief='groove')
        self.generate_report_button.pack(padx=40, pady=5, fill='x', expand=True)

    # View Frames
    def view_students(self):
        # Create student frame
        self.student_frame = tk.Frame(self.parent)
        self.student_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Create a style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        # Labels
        tk.Label(self.student_frame, text="University of Technology", font=("Helvetica", 10, "bold")).pack()
        tk.Label(self.student_frame, text="Student Listing").pack(pady=5)

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
        tree = ttk.Treeview(second_frame, show='headings', style="Treeview", height=23)

        # Add a Scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(second_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        # Configure the Treeview
        tree.configure(yscrollcommand=scrollbar.set)

        # Define columns
        columns = ("Student ID", "Student Name", "Student Email", "School", "Programme")
        tree["columns"] = columns

        # Format columns
        column_widths = [100, 150, 250, 230, 230]  # Adjust these values as needed
        for col, width in zip(columns, column_widths):
            tree.column(col, width=width)
            tree.heading(col, text=col, command=lambda _col=col: sort_column(tree, _col, False))

        # Insert data in table
        for student in db_manager.get_students():
            tree.insert("", "end", values=(student[0], student[1], student[2], student[3], student[4]))

        tree.pack()

        # Button configurations
        self.button_config(self.student_frame, tree, self.add_student, self.remove_student)

    def view_modules(self):
        # Create module frame
        self.module_frame = tk.Frame(self.parent)
        self.module_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Create a style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        # Labels
        tk.Label(self.module_frame, text="University of Technology", font=("Helvetica", 10, "bold")).pack()
        tk.Label(self.module_frame, text="Module Listing").pack(pady=5)

        # Create Canvas in new window
        canvas = tk.Canvas(self.module_frame)
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
        tree = ttk.Treeview(second_frame, show='headings', style="Treeview", height=23)

        # Add a Scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(second_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        # Configure the Treeview
        tree.configure(yscrollcommand=scrollbar.set)

        # Define columns
        columns = ("Module Code", "Module Name", "Accreditation")
        tree["columns"] = columns

        # Format columns
        column_widths = [200, 400, 150]  # Way to wide, leave as is for now
        for col, width in zip(columns, column_widths):
            tree.column(col, width=width)
            tree.heading(col, text=col, command=lambda _col=col: sort_column(tree, _col, False))

        # Insert data in table
        for module in db_manager.get_modules():
            tree.insert("", "end", values=(module[0], module[1], module[2]))

        tree.pack(padx=110)

        # Button configurations
        self.button_config(self.module_frame, tree, self.add_module, self.remove_module)

    # Insert Frames
    def add_student(self):
        print("Add Student")

    def add_details(self):
        print("Add Details")

    def add_module(self):
        print("Add Module")

    def remove_student(self, tree):
        selected_item = tree.selection()  # Get selected item
        if selected_item:
            student_id = str(tree.item(selected_item)["values"][0]).strip()
        else:
            # Display a dialog box to request the student ID
            student_id = simpledialog.askstring("Input", "Please enter the ID of the student to be deleted:",
                                                parent=self.student_frame)
            if student_id is None:  # If the user cancelled the dialog box
                return

        # Remove the student from the table
        if db_manager.remove_student(student_id) is True:
            if selected_item:
                tree.delete(selected_item)
            else:
                for item in tree.get_children():
                    tree_id = str(tree.item(item)["values"][0]).strip()  # Convert to string and remove spaces
                    if tree_id == student_id:
                        tree.delete(item)
                        break
        else:
            print("Failed to remove student.")

    def remove_module(self, tree):
        selected_item = tree.selection()  # Get selected item
        if selected_item:
            module_code = str(tree.item(selected_item)["values"][0]).strip()
        else:
            # Display a dialog box to request the module code
            module_code = simpledialog.askstring("Input", "Please enter the code of the module to be deleted:",
                                                 parent=self.module_frame)
            if module_code is None:  # If the user cancelled the dialog box
                return

        # Remove the module from the table
        if db_manager.remove_module(module_code) is True:
            if selected_item:
                tree.delete(selected_item)
            else:
                for item in tree.get_children():
                    tree_id = str(tree.item(item)["values"][0]).strip()  # Convert to string and remove spaces
                    if tree_id == module_code:
                        tree.delete(item)
                        break
        else:
            print("Failed to remove module.")

    def remove_details(self):
        print("Remove Details")

    def button_config(self, frame, tree, add, remove):
        add_button = tk.Button(frame, text="Add", command=add)
        remove_button = tk.Button(frame, text="Remove", command=lambda: remove(tree))
        close_button = tk.Button(frame, text="Close", command=self.close_view)

        button_width = 100  # width of the buttons
        button_spacing = 40  # space between the buttons
        total_width = 3 * button_width + 2 * button_spacing  # total width of all buttons and spaces

        # Center the buttons at the bottom of the window
        add_button.place(relx=0.5, rely=0.97, x=-total_width / 2, anchor='s', width=button_width)
        remove_button.place(relx=0.5, rely=0.97, x=-total_width / 2 + button_width + button_spacing, anchor='s',
                            width=button_width)
        close_button.place(relx=0.5, rely=0.97, x=-total_width / 2 + 2 * (button_width + button_spacing), anchor='s',
                           width=button_width)

    def close_view(self):  # we can keep editing this to close respective frames as we work
        # Check which view frame exists and remove it
        if self.student_frame is not None:
            self.student_frame.grid_forget()
            self.student_frame = None

        if self.module_frame is not None:
            self.module_frame.grid_forget()
            self.module_frame = None
