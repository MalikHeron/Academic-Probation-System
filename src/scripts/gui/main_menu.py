import logging
import tkinter as tk
from datetime import datetime
from tkinter import simpledialog, messagebox, ttk

import easygui

from scripts.database.queries import DatabaseManager
from scripts.gui.generate_report import GenerateReport
from scripts.gui.helpers import create_treeview, button_config, create_button, create_label_and_field, \
    create_buttons

db_manager = DatabaseManager()  # create an instance of DatabaseManager
global record_count  # global variable to keep track of the number of records


class MainMenu(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.record_count_label = None
        self.report_frame = None
        self.generate_report_button = None
        self.view_details_button = None
        self.student_frame = None
        self.details_frame = None
        self.add_details_frame = None
        self.module_frame = None
        self.view_modules_button = None
        self.add_module_frame = None
        self.add_student_button = None
        self.add_student_frame = None
        self.view_students_button = None
        self.title = None
        self.parent = parent
        self.record_count_var = tk.StringVar()
        self.setup_components()

    def setup_components(self):
        # title
        self.title = tk.Label(self, text="Main Menu", font=('Arial', 16, 'bold'))
        self.title.configure(foreground='black')
        self.title.pack(padx=20, pady=20, fill='x', expand=True)

        # student buttons
        self.view_students_button = create_button(self, "View Students", self.view_students)

        # module buttons
        self.view_modules_button = create_button(self, "View Modules", self.view_modules)

        # details button
        self.view_details_button = create_button(self, "View Details", self.view_details)

        # generate report button
        self.generate_report_button = create_button(self, "Generate Report", lambda: GenerateReport(self.parent),
                                                    bg_color='#936BE9')

    # View functions
    def view_students(self):
        # Close the existing frame
        self.close_view()

        # Create student frame
        self.student_frame = tk.Frame(self.parent)
        self.student_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Get data
        data = db_manager.get_students()

        # Set global record count
        global record_count
        record_count = len(data)

        # Labels
        tk.Label(self.student_frame, text="Student Listing", font=("Helvetica", 10, "bold")).pack()
        self.record_count_var.set(f"Number of Records: {record_count}")
        self.record_count_label = tk.Label(self.student_frame, textvariable=self.record_count_var)
        self.record_count_label.pack(pady=5)

        # Define columns
        columns = ("ID", "Student Name", "Student Email", "School", "Programme", "Advisor")
        column_widths = [50, 150, 250, 360, 300, 150]

        # Create Treeview
        tree = create_treeview(self.student_frame, columns, column_widths, 10, data=data)

        # Button configurations
        button_config(self.student_frame, tree, self.add_student, self.update_student, self.remove_student,
                      self.close_view)

    def view_modules(self):
        # Close the existing frame
        self.close_view()

        # Create module frame
        self.module_frame = tk.Frame(self.parent)
        self.module_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Get data
        data = db_manager.get_modules()

        # Set global record count
        global record_count
        record_count = len(data)

        # Labels
        tk.Label(self.module_frame, text="Module Listing", font=("Helvetica", 10, "bold")).pack()
        self.record_count_var.set(f"Number of Records: {record_count}")
        self.record_count_label = tk.Label(self.module_frame, textvariable=self.record_count_var)
        self.record_count_label.pack(pady=5)

        # Define columns
        columns = ("Module Code", "Module Name", "Accreditation")
        column_widths = [200, 400, 150]

        # Create Treeview
        tree = create_treeview(self.module_frame, columns, column_widths, 265, data=data)

        # Button configurations
        button_config(self.module_frame, tree, self.add_module, self.update_module, self.remove_module,
                      self.close_view)

    def view_details(self):
        # Close the existing frame
        self.close_view()

        # Create module frame
        self.details_frame = tk.Frame(self.parent)
        self.details_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Get data
        data = db_manager.get_details()

        # Set global record count
        global record_count
        record_count = len(data)

        # Labels
        tk.Label(self.details_frame, text="Student Module Details", font=("Helvetica", 10, "bold")).pack()
        self.record_count_var.set(f"Number of Records: {record_count}")
        self.record_count_label = tk.Label(self.details_frame, textvariable=self.record_count_var)
        self.record_count_label.pack(pady=5)

        # Define columns
        columns = ("Student ID", "Module", "Grade Point Average", "Semester", "Year")
        column_widths = [100, 200, 200, 150, 150]

        # Create Treeview
        tree = create_treeview(self.details_frame, columns, column_widths, 240, data=data)

        # Button configurations
        button_config(self.details_frame, tree, self.add_details, self.update_details, self.remove_details,
                      self.close_view)

    # Student Functions
    def create_student_frame(self, title, submit_action):
        # Close the existing frame
        self.close_view()

        # Create the student frame
        self.add_student_frame = tk.Frame(self.parent, padx=60, pady=20)
        self.add_student_frame.grid(row=0, column=1, sticky="nsew")

        # Padding and field dimensions
        x_padding, y_padding, f_width, l_width = 5, 20, 35, 11

        # Labels
        tk.Label(self.add_student_frame, text=title,
                 font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        # Student ID label and field
        student_id_field = create_label_and_field(self.add_student_frame, "ID Number", 2, f_width=f_width - 1)

        # Student Name label and field
        student_name_field = create_label_and_field(self.add_student_frame, "Full Name", 3, f_width=f_width - 1)

        # Student Email label and field
        student_email_field = create_label_and_field(self.add_student_frame, "Email", 4, f_width=f_width - 1)

        # School label and field
        tk.Label(self.add_student_frame, text="School", width=l_width, anchor="w",
                 font=("Helvetica", 12)).grid(row=5, column=0, padx=x_padding, pady=y_padding)
        school_list = db_manager.get_schools()
        school_names = [school[2] for school in school_list]  # Extract school names
        school_var = tk.StringVar()  # Create a StringVar to hold the school value
        school_field = ttk.Combobox(self.add_student_frame, font=("Helvetica", 11), state="readonly",
                                    values=school_names, width=f_width, textvariable=school_var)
        school_field.grid(row=5, column=1)

        # Programme label and field
        tk.Label(self.add_student_frame, text="Programme", width=l_width, anchor="w",
                 font=("Helvetica", 12)).grid(row=6, column=0, padx=x_padding, pady=y_padding)
        programme_var = tk.StringVar()  # Create a StringVar to hold the programme value
        programme_field = ttk.Combobox(self.add_student_frame, font=("Helvetica", 11), state="disabled",
                                       values=[], width=f_width, textvariable=programme_var)
        programme_field.grid(row=6, column=1)

        # Advisor label and field
        tk.Label(self.add_student_frame, text="Advisor", width=l_width, anchor="w",
                 font=("Helvetica", 12)).grid(row=7, column=0, padx=x_padding, pady=y_padding)
        advisor_list = db_manager.get_advisors()
        advisor_names = [advisor[1] for advisor in advisor_list]  # Extract school names
        advisor_field = ttk.Combobox(self.add_student_frame, font=("Helvetica", 11), state="readonly",
                                     values=advisor_names, width=f_width)
        advisor_field.grid(row=7, column=1)

        # Monitor changes to the school field and update the programme field accordingly
        def update_programmes(*args):
            school = school_var.get()
            if school:
                faculty = school_list[school_names.index(school)][0]  # Get the faculty for the selected school
                programme_field['state'] = 'readonly'  # Enable the programme field
                programme_list = db_manager.get_programmes(faculty)  # Get programmes for the selected school
                programme_names = [programme[3] for programme in programme_list]  # Extract programme names
                programme_var.set('')  # Clear the current programme value
                programme_field['values'] = programme_names  # Update the programme field values
            else:
                programme_field['state'] = 'disabled'  # Disable the programme field
                programme_var.set('')  # Clear the current programme value
                programme_field['values'] = []  # Clear the programme field values

        school_var.trace('w', update_programmes)  # Call update_programmes when the school value changes

        # Create buttons
        create_buttons(self.add_student_frame, [student_id_field,
                                                student_name_field,
                                                student_email_field,
                                                school_field,
                                                programme_field,
                                                advisor_field], 8, submit_action, self.clear_fields, self.close_view)

        return student_id_field, student_name_field, student_email_field, school_field, programme_field, advisor_field

    def add_student(self):
        # Define the submit action
        def submit_action():
            self.validate({"ID": (student_id_field, "int"),
                           "Full Name": (student_name_field, "str"),
                           "Email": (student_email_field, "str"),
                           "School": (school_field, "str"),
                           "Programme": (programme_field, "str"),
                           "Advisor": (advisor_field, "str")},
                          self.add_student_to_db)

        # Create the student frame
        student_id_field, student_name_field, student_email_field, school_field, programme_field, advisor_field \
            = self.create_student_frame("Add Student", submit_action)

    def update_student(self, tree):
        # Get the selected item from the tree
        selected_item = tree.selection()

        # Define the submit action
        def submit_action():
            self.validate({"ID": (student_id_field, "int"),
                           "Full Name": (student_name_field, "str"),
                           "Email": (student_email_field, "str"),
                           "School": (school_field, "str"),
                           "Programme": (programme_field, "str"),
                           "Advisor": (advisor_field, "str")},
                          self.update_student_in_db)

        # Create the student frame
        student_id_field, student_name_field, student_email_field, school_field, programme_field, advisor_field \
            = self.create_student_frame("Update Student", submit_action)

        # Populate fields
        student_id_field.insert(0, str(tree.item(selected_item)["values"][0]).strip())
        student_id_field.configure(state="disabled")
        student_name_field.insert(0, str(tree.item(selected_item)["values"][1]).strip())
        student_email_field.insert(0, str(tree.item(selected_item)["values"][2]).strip())
        school_field.set(str(tree.item(selected_item)["values"][3]).strip())
        programme_field.set(str(tree.item(selected_item)["values"][4]).strip())
        advisor_field.set(str(tree.item(selected_item)["values"][5]).strip())

    # Details functions
    def create_details_frame(self, title, submit_action):
        # Close the existing frame
        self.close_view()

        # Create details frame
        self.add_details_frame = tk.Frame(self.parent, padx=100, pady=20)
        self.add_details_frame.grid(row=0, column=1, sticky="nsew")

        # Padding
        x_padding, y_padding, f_width, l_width = 20, 20, 20, 11

        # Labels
        tk.Label(self.add_details_frame, text=title,
                 font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        # ID number label and field
        tk.Label(self.add_details_frame, text="ID Number", width=l_width, anchor="w",
                 font=("Helvetica", 12)).grid(row=2, column=0, padx=x_padding, pady=y_padding)
        if title == "Add Details":
            student_list = db_manager.get_students()
            student_ids = [student[0] for student in student_list]  # Extract module codes
            id_field = ttk.Combobox(self.add_details_frame, font=("Helvetica", 11), state="readonly",
                                    values=student_ids, width=f_width)
            id_field.grid(row=2, column=1)

            # Module label and field
            tk.Label(self.add_details_frame, text="Module", width=l_width, anchor="w",
                     font=("Helvetica", 12)).grid(row=3, column=0, padx=x_padding, pady=y_padding)
            module_list = db_manager.get_modules()
            module_names = [module[1] for module in module_list]  # Extract module names
            module_field = ttk.Combobox(self.add_details_frame, font=("Helvetica", 11), state="readonly",
                                        values=module_names, width=f_width)
            module_field.grid(row=3, column=1)
        else:
            id_field = create_label_and_field(self.add_details_frame, "ID Number", 2, f_width=f_width)
            module_field = create_label_and_field(self.add_details_frame, "Module", 3, f_width=f_width)

        # Grade Point label and field
        gpa_field = create_label_and_field(self.add_details_frame, "GPA", 4, f_width=f_width)

        # Semester label and field
        tk.Label(self.add_details_frame, text="Semester", width=l_width, anchor="w",
                 font=("Helvetica", 12)).grid(row=5, column=0, padx=x_padding, pady=y_padding)
        semester_field = ttk.Combobox(self.add_details_frame, font=("Helvetica", 11), state="readonly",
                                      values=["1", "2"], width=f_width)
        semester_field.grid(row=5, column=1)

        # Year label and field
        tk.Label(self.add_details_frame, text="Year", width=l_width, anchor="w",
                 font=("Helvetica", 12)).grid(row=6, column=0, padx=x_padding, pady=y_padding)
        current_year = datetime.now().year  # Get the current year
        year_var = tk.StringVar()  # Create a StringVar
        year_field = tk.Spinbox(self.add_details_frame, font=('Helvetica', 11, 'normal'), from_=2016,
                                to=current_year, width=f_width,
                                textvariable=year_var)  # Associate the StringVar with the Spinbox
        year_field.grid(row=6, column=1, padx=x_padding, pady=y_padding)

        # Create buttons
        create_buttons(self.add_details_frame, [id_field, gpa_field, module_field, semester_field,
                                                year_field], 7, submit_action, self.clear_fields, self.close_view)

        return id_field, gpa_field, module_field, semester_field, year_field, year_var

    def add_details(self):
        # Define the submit action
        def submit_action():
            self.validate({
                "ID": (id_field, "int"),
                "Module": (module_field, "str"),
                "GPA": (gpa_field, "float"),
                "Semester": (semester_field, "int"),
                "Year": (year_field, "int")
            }, self.add_detail_to_db)

        # Create the details frame
        id_field, gpa_field, module_field, semester_field, year_field, year_var \
            = self.create_details_frame("Add Details", submit_action)

    def update_details(self, tree):
        # Get the selected item from the tree
        selected_item = tree.selection()

        # Define the submit action
        def submit_action():
            self.validate({
                "ID": (id_field, "int"),
                "Module": (module_field, "str"),
                "GPA": (gpa_field, "float"),
                "Semester": (semester_field, "int"),
                "Year": (year_field, "int")
            }, self.update_detail_in_db)

        # Create the details frame
        id_field, gpa_field, module_field, semester_field, year_field, year_var \
            = self.create_details_frame("Update Details", submit_action)

        # Populate fields
        id_field.insert(0, str(tree.item(selected_item)["values"][0]).strip())
        id_field.configure(state="disabled")
        module_field.insert(0, str(tree.item(selected_item)["values"][1]).strip())
        module_field.configure(state="disabled")
        gpa_field.insert(0, str(tree.item(selected_item)["values"][2]).strip())
        semester_field.set(str(tree.item(selected_item)["values"][3]).strip())
        year_var.set(str(tree.item(selected_item)["values"][4]).strip())

    # Module functions
    def create_module_frame(self, title, submit_action):
        # Close the existing frame
        self.close_view()

        # Create the module frame
        self.add_module_frame = tk.Frame(self.parent, padx=100, pady=20)
        self.add_module_frame.grid(row=0, column=1, sticky="nsew")

        # Padding and field dimensions
        x_padding, y_padding, f_width, f_height, l_width = 5, 20, 25, 2, 11

        # Labels
        tk.Label(self.add_module_frame, text=title,
                 font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        # Module Code label and field
        mod_code_field = create_label_and_field(self.add_module_frame, "Module Code", 2)

        # Module Name label and field
        mod_name_field = create_label_and_field(self.add_module_frame, "Module Name", 3)

        # Credits label and field
        tk.Label(self.add_module_frame, text="Credits", width=l_width, anchor="w",
                 font=("Helvetica", 12)).grid(row=4, column=0, padx=x_padding, pady=y_padding)
        mod_credits_field = ttk.Combobox(self.add_module_frame, font=("Helvetica", 12), state="readonly",
                                         values=["1", "2", "3", "4"], width=f_width - 2)
        mod_credits_field.grid(row=4, column=1)

        # Create buttons
        create_buttons(self.add_module_frame, [mod_code_field, mod_name_field, mod_credits_field], 5, submit_action,
                       self.clear_fields, self.close_view)

        return mod_code_field, mod_name_field, mod_credits_field

    def add_module(self):
        # Define the submit action
        def submit_action():
            self.validate({
                "Module Code": (mod_code_field, "str"),
                "Module Name": (mod_name_field, "str"),
                "Credits": (mod_credits_field, "int")
            }, self.add_module_to_db)

        # Create the module frame
        mod_code_field, mod_name_field, mod_credits_field = self.create_module_frame("Add Module", submit_action)

    def update_module(self, tree):
        # Get the selected item from the tree
        selected_item = tree.selection()

        # Define the submit action
        def submit_action():
            self.validate({
                "Module Code": (mod_code_field, "str"),
                "Module Name": (mod_name_field, "str"),
                "Credits": (mod_credits_field, "int")
            }, self.update_module_in_db)

        # Create the module frame
        mod_code_field, mod_name_field, mod_credits_field \
            = self.create_module_frame("Update Module", submit_action)

        # Populate fields
        mod_code_field.insert(0, str(tree.item(selected_item)["values"][0]).strip())
        mod_code_field.configure(state="disabled")
        mod_name_field.insert(0, str(tree.item(selected_item)["values"][1]).strip())
        mod_credits_field.set(str(tree.item(selected_item)["values"][2]).strip())

    # Helper functions
    @staticmethod
    def clear_fields(*fields):
        # Clear all fields and set to default values
        for field in fields:
            if isinstance(field, tk.Text):
                field.delete("1.0", tk.END)
            elif isinstance(field, tk.ttk.Combobox):
                field.set("")
            elif isinstance(field, tk.Entry):
                field.delete(0, tk.END)
            elif isinstance(field, tk.StringVar):
                field.set("")
            elif isinstance(field, tk.Spinbox):
                field.delete(0, tk.END)
                field.insert(0, "2016")

    @staticmethod
    def add_to_db(add_record, data, success_message, error_message):
        # Insert the record into the database
        success = add_record(*data)
        if success:
            # Display a success message
            messagebox.showinfo("Success", success_message)
        else:
            # Display an error message
            messagebox.showerror("Error", error_message)

    @staticmethod
    def update_in_db(data, table_name, success_message, error_message):
        # Insert the record into the database
        success = db_manager.update_record(data, table_name)
        if success:
            # Display a success message
            messagebox.showinfo("Success", success_message)
        else:
            # Display an error message
            messagebox.showerror("Error", error_message)

    # Add functions
    def add_student_to_db(self, validated_fields):
        self.add_to_db(db_manager.insert_student, (validated_fields["ID"], validated_fields["Full Name"],
                                                   validated_fields["Email"], validated_fields["School"],
                                                   validated_fields["Programme"], validated_fields["Advisor"]),
                       "Student record added successfully.",
                       "Failed to add student record.")

    def add_detail_to_db(self, validated_fields):
        self.add_to_db(db_manager.insert_detail, (validated_fields["ID"], validated_fields["Module"],
                                                  validated_fields["GPA"], validated_fields["Semester"],
                                                  validated_fields["Year"]),
                       "Detail record added successfully.",
                       "Failed to add detail record.")

    def add_module_to_db(self, validated_fields):
        self.add_to_db(db_manager.insert_module, (validated_fields["Module Code"], validated_fields["Module Name"],
                                                  validated_fields["Credits"]),
                       "Module record added successfully.",
                       "Failed to add module record.")

    # Update functions
    def update_student_in_db(self, validated_fields):
        self.update_in_db((validated_fields["ID"], validated_fields["Full Name"],
                           validated_fields["Email"], validated_fields["School"],
                           validated_fields["Programme"], validated_fields["Advisor"]),
                          "student",
                          "Student record updated successfully.",
                          "Failed to update student record.")
        self.close_view()

    def update_detail_in_db(self, validated_fields):
        self.update_in_db((validated_fields["ID"], validated_fields["Module"],
                           validated_fields["GPA"], validated_fields["Semester"], validated_fields["Year"]),
                          "details",
                          "Module detail record updated successfully.",
                          "Failed to update module detail record.")
        self.close_view()

    def update_module_in_db(self, validated_fields):
        self.update_in_db((validated_fields["Module Code"], validated_fields["Module Name"],
                           validated_fields["Credits"]),
                          "module",
                          "Module record updated successfully.",
                          "Failed to update module record.")
        self.close_view()

    # Remove functions
    def remove_item(self, tree, remove_func, dialog_title, dialog_prompt, parent_frame, fields=None):
        # Set global record count
        global record_count

        # Get the selected item from the tree
        selected_item = tree.selection()

        # If an item is selected, get its values
        if selected_item:
            # If fields is None, get the first value
            if fields is None:
                values = str(tree.item(selected_item)["values"][0]).strip()
            else:
                # Otherwise, get all the values
                student_id = str(tree.item(selected_item)["values"][0]).strip()
                module_code = str(tree.item(selected_item)["values"][1]).strip()
                semester = str(tree.item(selected_item)["values"][3]).strip()
                values = [student_id, module_code, semester]
        else:
            # If no item is selected, display a dialog box to request the values
            if fields is None:
                # Display a dialog box to request the student ID
                values = simpledialog.askstring(dialog_title, dialog_prompt, parent=parent_frame)

                # If the user cancelled the dialog box, return
                if values is None:
                    return
            else:
                # Display a dialog box to request multiple values
                values = easygui.multenterbox(dialog_prompt, dialog_title, fields)

                # If the user cancelled the dialog box, return
                if values is None:
                    return

        # If fields is None, call the remove function with a single argument
        # Otherwise, unpack the values and pass them as arguments
        if fields is None:
            removed = remove_func(values)
        else:
            removed = remove_func(*values)

        # If the item was successfully removed
        if removed is True:
            # If an item was selected, delete it from the tree
            if selected_item:
                tree.delete(selected_item)
            else:
                # If no item was selected, find and delete the item from the tree
                for item in tree.get_children():
                    # Get the first value of the item
                    tree_id = str(tree.item(item)["values"][0]).strip()

                    # If fields is None, compare the first value
                    if fields is None:
                        if tree_id == values:
                            tree.delete(item)
                            break
                    else:
                        # Otherwise, compare all the values
                        tree_code = str(tree.item(item)["values"][1]).strip()
                        tree_sem = str(tree.item(item)["values"][3]).strip()

                        if tree_id == values[0] and tree_code == values[1] and tree_sem == values[2]:
                            tree.delete(item)
                            break

            # Decrement the record count
            if record_count > 0:
                # Decrement the record count
                record_count -= 1
                # Update the record count label
                self.record_count_var.set(f"Number of Records: {record_count}")

            # Refresh the tree view
            tree.update_idletasks()
        else:
            # Display an error message
            messagebox.showerror("Error", "Failed to remove record.")

    def remove_student(self, tree):
        self.remove_item(tree, db_manager.remove_student, "Input", "Please enter the ID of the student to be deleted:",
                         self.student_frame)

    def remove_module(self, tree):
        self.remove_item(tree, db_manager.remove_module, "Input", "Please enter the code of the module to be deleted:",
                         self.module_frame)

    def remove_details(self, tree):
        self.remove_item(tree, db_manager.remove_details, "Input", "Enter values for the fields.", self.details_frame,
                         ["Student ID", "Module Name", "Semester"])

    def validate(self, fields, submit_func):
        validated_fields = {}  # Store the validated fields
        field_widgets = []  # Store the field widgets

        for field_name, (input_field, validation_type) in fields.items():
            try:
                # Get the input value
                input_value = input_field.get()
                field_widgets.append(input_field)  # Add the input field widget to the list
                if validation_type == "int":
                    # Validate as an integer
                    if input_value.isdigit():
                        validated_fields[field_name] = input_value
                    else:
                        raise ValueError("is not a valid integer.")
                elif validation_type == "str":
                    # Validate as a non-empty string
                    if input_value.strip():
                        validated_fields[field_name] = input_value
                    else:
                        raise ValueError("cannot be empty.")
                elif validation_type == "float":
                    # Validate as a decimal number
                    if input_value.replace(".", "", 1).isdigit():
                        if float(input_value) < 0 or float(input_value) > 4:
                            raise ValueError("must be a decimal number between 0 and 4.")
                        validated_fields[field_name] = input_value
                    else:
                        raise ValueError("is not a valid decimal number.")
                # Add more validation types as needed
                else:
                    # Unknown validation type
                    raise ValueError(f"Unknown validation type for {field_name}.")
            except ValueError as e:
                # If validation fails, show an error message and return
                tk.messagebox.showerror("Error", f"{field_name}: {e}")
                return
            except Exception as e:
                # Handle any unexpected errors
                tk.messagebox.showerror("Error", "Failed to validate input.")
                logging.error("An error occurred in validating input:", e)
                return

        # If all fields are successfully validated, call the submit function
        submit_func(validated_fields)
        self.clear_fields(*field_widgets)  # Clear all fields

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

        elif self.add_student_frame is not None:
            self.add_student_frame.grid_forget()
            self.add_student_frame = None
            self.view_students()

        elif self.add_module_frame is not None:
            self.add_module_frame.grid_forget()
            self.add_module_frame = None
            self.view_modules()

        elif self.add_details_frame is not None:
            self.add_details_frame.grid_forget()
            self.add_details_frame = None
            self.view_details()
