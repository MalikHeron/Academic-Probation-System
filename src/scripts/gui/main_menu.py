import tkinter as tk
from tkinter import simpledialog

import easygui  # pip install easygui

from scripts.gui.generate_report import GenerateReportFrame
from scripts.gui.helpers import create_treeview, button_config
from scripts.database.queries import DatabaseManager

db_manager = DatabaseManager()  # create an instance of DatabaseManager


class MainMenu(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.report_frame = None
        self.generate_report_button = None
        self.view_details_button = None
        self.student_frame = None
        self.details_frame = None
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
        self.view_details_button = tk.Button(self, text="View Details", command=self.view_details)
        self.view_details_button.configure(background='#61CBEC', foreground='#000000', font=('Arial', 12, 'normal'),
                                           relief='groove')
        self.view_details_button.pack(padx=40, pady=5, fill='x', expand=True)

        # generate report button
        self.generate_report_button = tk.Button(self, text="Generate Report",
                                                command=lambda: GenerateReportFrame(self.parent))
        self.generate_report_button.configure(background='#936BE9', foreground='#000000', font=('Arial', 12, 'normal'),
                                              relief='groove')
        self.generate_report_button.pack(padx=40, pady=5, fill='x', expand=True)

    # View Frames
    def view_students(self):
        # Create student frame
        self.student_frame = tk.Frame(self.parent)
        self.student_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Labels
        tk.Label(self.student_frame, text="University of Technology", font=("Helvetica", 10, "bold")).pack()
        tk.Label(self.student_frame, text="Student Listing").pack(pady=5)

        # Define columns
        columns = ("Student ID", "Student Name", "Student Email", "School", "Programme")
        column_widths = [100, 150, 250, 230, 230]

        # Get data
        data = db_manager.get_students()

        # Create Treeview
        tree = create_treeview(self.student_frame, columns, column_widths, 10, data=data)

        # Button configurations
        button_config(self.student_frame, tree, self.add_student, self.remove_student, self.close_view)

    def view_modules(self):
        # Create module frame
        self.module_frame = tk.Frame(self.parent)
        self.module_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Labels
        tk.Label(self.module_frame, text="University of Technology", font=("Helvetica", 10, "bold")).pack()
        tk.Label(self.module_frame, text="Module Listing").pack(pady=5)

        # Define columns
        columns = ("Module Code", "Module Name", "Accreditation")
        column_widths = [200, 400, 150]

        # Get data
        data = db_manager.get_modules()

        # Create Treeview
        tree = create_treeview(self.module_frame, columns, column_widths, 115, data=data)

        # Button configurations
        button_config(self.module_frame, tree, self.add_module, self.remove_module, self.close_view)

    def view_details(self):
        # Create module frame
        self.details_frame = tk.Frame(self.parent)
        self.details_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Labels
        tk.Label(self.details_frame, text="University of Technology", font=("Helvetica", 10, "bold")).pack()
        tk.Label(self.details_frame, text="Student Module Details").pack(pady=5)

        # Define columns
        columns = ("Student ID", "Module Code", "Grade Point", "Semester", "Year")
        column_widths = [100, 200, 150, 150, 150]

        # Get data
        data = db_manager.get_details()

        # Create Treeview
        tree = create_treeview(self.details_frame, columns, column_widths, 115, data=data)

        # Button configurations
        button_config(self.details_frame, tree, self.add_details, self.remove_details, self.close_view)

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

    def remove_details(self, tree):
        selected_item = tree.selection()  # Get selected item
        if selected_item:
            student_id = str(tree.item(selected_item)["values"][0]).strip()
            module_code = str(tree.item(selected_item)["values"][1]).strip()
            semester = str(tree.item(selected_item)["values"][2]).strip()
        else:
            fields = ["Student ID", "Module Code", "Semester"]
            values = easygui.multenterbox("Enter values for the fields.", "Input", fields)
            if values is None:  # If the user cancelled the dialog box
                return
            student_id, module_code, semester = values

        # Remove the module from the table
        if db_manager.remove_details(student_id, module_code, semester) is True:
            if selected_item:
                tree.delete(selected_item)
            else:
                for item in tree.get_children():
                    tree_id = str(tree.item(item)["values"][0]).strip()
                    tree_code = str(tree.item(item)["values"][1]).strip()
                    tree_sem = str(tree.item(item)["values"][2]).strip()
                    # Convert to string and remove spaces
                    if tree_id == student_id and tree_code == module_code and tree_sem == semester:
                        tree.delete(item)
                        break
        else:
            print("Failed to remove details.")

    def close_view(self):  # we can keep editing this to close respective frames as we work
        # Check which view frame exists and remove it
        if self.student_frame is not None:
            self.student_frame.grid_forget()
            self.student_frame = None

        elif self.module_frame is not None:
            self.module_frame.grid_forget()
            self.module_frame = None

        elif self.details_frame is not None:
            self.details_frame.grid_forget()
            self.details_frame = None
