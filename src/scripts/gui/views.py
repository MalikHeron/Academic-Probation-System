import tkinter as tk
from tkinter import messagebox, ttk

from scripts.database.queries import DatabaseManager
from scripts.gui.dialogs import Dialog
from scripts.gui.helpers import Helpers

db_manager = DatabaseManager()  # create an instance of DatabaseManager
global student_count  # keep track of the number of student records
global module_count  # keep track of the number of module records
global details_count  # keep track of the number of details records


class Views(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.search_bar = None
        self.data = None
        self.tree = None
        self.record_count_label = None
        self.student_frame = None
        self.details_frame = None
        self.module_frame = None
        self.helpers = Helpers()  # create an instance of Helpers
        self.parent = parent
        self.record_count_var = tk.StringVar()

    # View functions
    def student_view(self):
        # Create student frame
        self.student_frame = ttk.Frame(self.parent)
        self.student_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Get data
        self.data = db_manager.get_students()

        # Set global record count
        global student_count
        student_count = len(self.data)

        # Labels
        self.record_count_var.set(f"Number of Records: {student_count}")
        self.record_count_label = ttk.Label(self.student_frame, textvariable=self.record_count_var)
        self.record_count_label.pack(side="top", pady=(10, 0))

        # Define columns
        columns = ("ID", "Student Name", "Student Email", "School", "Programme", "Advisor")
        column_widths = [50, 150, 250, 380, 300, 150]
        column_alignments = ["center", "w", "w", "w", "w", "w"]

        # Create search bar
        self.search_bar = self.helpers.create_search_bar(self.student_frame)

        # Create Treeview
        self.tree = self.helpers.create_view_table(self.student_frame, columns, column_widths, column_alignments,
                                                   data=self.data)

        # Update search function whenever search text is changed
        self.update_search()

        # Pack the tree
        self.tree.pack(padx=10)

        # Button configurations
        self.helpers.create_crud_buttons(self.student_frame, self.tree, db_manager.get_students, self.add_student,
                                         self.update_student,
                                         self.remove_student,
                                         self.refresh)

        return self.student_frame

    def module_view(self):
        # Create module frame
        self.module_frame = ttk.Frame(self.parent)
        self.module_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Get data
        self.data = db_manager.get_modules()

        # Set global record count
        global module_count
        module_count = len(self.data)

        # Labels
        self.record_count_var.set(f"Number of Records: {module_count}")
        self.record_count_label = ttk.Label(self.module_frame, textvariable=self.record_count_var)
        self.record_count_label.pack(side="top", pady=(10, 0))

        # Define columns
        columns = ("Module Code", "Module Name", "Accreditation")
        column_widths = [200, 400, 150]
        column_alignments = ["center", "w", "center"]

        # Create search bar
        self.search_bar = self.helpers.create_search_bar(self.module_frame)

        # Create Treeview
        self.tree = self.helpers.create_view_table(self.module_frame, columns, column_widths, column_alignments,
                                                   data=self.data,
                                                   pad_x=530)

        # Update search function whenever search text is changed
        self.update_search()

        # Pack the tree
        self.tree.pack(padx=10)

        # Button configurations
        self.helpers.create_crud_buttons(self.module_frame, self.tree, db_manager.get_modules, self.add_module,
                                         self.update_module,
                                         self.remove_module, self.refresh)

        return self.module_frame

    def details_view(self):
        # Create module frame
        self.details_frame = ttk.Frame(self.parent)
        self.details_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Get data
        data = db_manager.get_details()

        # Set global record count
        global details_count
        details_count = len(data)

        # Labels
        self.record_count_var.set(f"Number of Records: {details_count}")
        self.record_count_label = ttk.Label(self.details_frame, textvariable=self.record_count_var)
        self.record_count_label.pack(side="top", pady=(10, 0))

        # Define columns
        columns = ("Student ID", "Module", "Grade Point Average", "Semester", "Year")
        column_widths = [100, 250, 200, 150, 150]
        column_alignments = ["center", "w", "center", "center", "center"]

        # Create search bar
        self.search_bar = self.helpers.create_search_bar(self.details_frame)

        # Create Treeview
        self.tree = self.helpers.create_view_table(self.details_frame, columns, column_widths, column_alignments,
                                                   data=data,
                                                   pad_x=430)

        # Update search function whenever search text is changed
        self.update_search()

        # Pack the tree
        self.tree.pack(padx=10)

        # Button configurations
        self.helpers.create_crud_buttons(self.details_frame, self.tree, db_manager.get_details, self.add_details,
                                         self.update_details,
                                         self.remove_details, self.refresh)

        return self.details_frame

    def create_dialog(self, dialog_type, db_action, selected_item=None):
        # Create an instance of Dialog
        dialog = Dialog(self)
        fields = []  # Create an empty list to store the fields

        if dialog_type == "student":
            def submit_action():
                self.helpers.validate({"ID": (id_field, "int"),
                                       "Full Name": (name_field, "str"),
                                       "Email": (email_field, "email"),
                                       "School": (school_field, "str"),
                                       "Programme": (programme_field, "str"),
                                       "Advisor": (advisor_field, "str")}, db_action)

            frame, id_field, name_field, email_field, school_field, programme_field, advisor_field \
                = dialog.student_dialog("Add Student", submit_action)
            fields = [id_field, name_field, email_field, school_field, programme_field, advisor_field]
        elif dialog_type == "module":
            def submit_action():
                self.helpers.validate({
                    "Module Code": (code_field, "str"),
                    "Module Name": (name_field, "str"),
                    "Credits": (credits_field, "int")
                }, self.update_module_in_db)

            frame, code_field, name_field, credits_field = dialog.module_dialog("Add Module", submit_action)
            fields = [code_field, name_field, credits_field]
        elif dialog_type == "details":
            def submit_action():
                self.helpers.validate({
                    "ID": (id_field, "int"),
                    "Module": (module_field, "str"),
                    "GPA": (gpa_field, "float"),
                    "Semester": (semester_field, "int"),
                    "Year": (year_field, "int")
                }, db_action)

            frame, id_field, gpa_field, module_field, semester_field, year_field, year_var \
                = dialog.details_dialog("Add Details", submit_action)
            fields = [id_field, gpa_field, module_field, semester_field, year_field, year_var]

        if selected_item is not None:
            for i, field in enumerate(fields):
                if hasattr(field, 'set'):
                    field.set(str(self.tree.item(selected_item)["values"][i]).strip())
                else:
                    field.insert(0, str(self.tree.item(selected_item)["values"][i]).strip())
                if i < 2:  # ID and Module fields are disabled for updates
                    field.configure(state="disabled")

        dialog.wait_window()  # This will wait until the dialog is destroyed

    def add_student(self):
        # Call the dialog box with no arguments
        self.create_dialog("student", self.add_student_to_db)

    def update_student(self):
        # Get the selected item from the tree
        selected_item = self.tree.selection()
        # Call the dialog box with the selected item
        self.create_dialog("student", self.update_student_in_db, selected_item)

    def add_module(self):
        # Call the dialog box with no arguments
        self.create_dialog("module", self.add_module_to_db)

    def update_module(self):
        # Get the selected item from the tree
        selected_item = self.tree.selection()
        # Call the dialog box with the selected item
        self.create_dialog("module", self.update_module_in_db, selected_item)

    def add_details(self):
        self.create_dialog("details", self.add_detail_to_db)

    def update_details(self):
        # Get the selected item from the tree
        selected_item = self.tree.selection()
        # Call the dialog box with the selected item
        self.create_dialog("details", self.update_detail_in_db, selected_item)

    # Refresh functions
    def refresh(self, frame, get_data_func):
        # Clear the tree
        self.tree.delete(*self.tree.get_children())

        # Get data
        self.data = get_data_func()

        match get_data_func:
            case db_manager.get_students:
                global student_count
                student_count = len(self.data)
                record_count = student_count
            case db_manager.get_details:
                global details_count
                details_count = len(self.data)
                record_count = details_count
            case db_manager.get_modules:
                global module_count
                module_count = len(self.data)
                record_count = module_count

        # Update the record count
        frame.after(100, lambda: self.record_count_var.set(f"Number of Records: {record_count}"))

        # Insert data in table
        for item in self.data:
            self.tree.insert("", "end", values=item)

        # Update the tree view
        self.tree.update_idletasks()

    def add_to_db(self, add_record, data, success_message, error_message):
        # Insert the record into the database
        success = add_record(*data)
        if success:
            # Display a success message
            messagebox.showinfo("Success", success_message)
            match add_record:
                case db_manager.insert_student:
                    self.refresh(self.student_frame, db_manager.get_students)
                case db_manager.insert_detail:
                    self.refresh(self.details_frame, db_manager.get_details)
                case db_manager.insert_module:
                    self.refresh(self.module_frame, db_manager.get_modules)
        else:
            # Display an error message
            messagebox.showerror("Error", error_message)

    def update_in_db(self, data, table_name, success_message, error_message):
        # Insert the record into the database
        success = db_manager.update_record(data, table_name)
        if success:
            # Display a success message
            messagebox.showinfo("Success", success_message)
            match table_name:
                case "student":
                    self.refresh(self.student_frame, db_manager.get_students)
                case "details":
                    self.refresh(self.details_frame, db_manager.get_details)
                case "module":
                    self.refresh(self.module_frame, db_manager.get_modules)
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

    def update_detail_in_db(self, validated_fields):
        self.update_in_db((validated_fields["ID"], validated_fields["Module"],
                           validated_fields["GPA"], validated_fields["Semester"], validated_fields["Year"]),
                          "details",
                          "Module detail record updated successfully.",
                          "Failed to update module detail record.")

    def update_module_in_db(self, validated_fields):
        self.update_in_db((validated_fields["Module Code"], validated_fields["Module Name"],
                           validated_fields["Credits"]),
                          "module",
                          "Module record updated successfully.",
                          "Failed to update module record.")

    # Remove functions
    def remove_item(self, remove_func, parent_frame, option=1, dialog_prompt=None):
        # Get the selected item from the tree
        selected_items = self.tree.selection()

        # If an item is selected, get its values
        if selected_items:
            if messagebox.askokcancel("Confirm", "Are you sure you want to remove the selected item(s)?"):
                for selected_item in selected_items:
                    # If fields is None, get the first value
                    if option == 1:
                        values = str(self.tree.item(selected_item)["values"][0]).strip()
                    else:
                        # Otherwise, get all the values
                        student_id = str(self.tree.item(selected_item)["values"][0]).strip()
                        module_code = str(self.tree.item(selected_item)["values"][1]).strip()
                        semester = str(self.tree.item(selected_item)["values"][3]).strip()
                        values = [student_id, module_code, semester]

                    # Call the remove function with the appropriate arguments
                    if option == 1:
                        removed = remove_func(values)
                    else:
                        removed = remove_func(*values)

                    # If the item was successfully removed, delete it from the tree
                    if removed is True:
                        self.tree.delete(selected_item)
                    else:
                        # Display an error message
                        messagebox.showerror("Error", "Failed to remove record.")
            else:
                return
        else:
            # If no item is selected, display a dialog box to request the values
            if option == 1:
                # Display a dialog box to request a single value
                dialog = Dialog(parent_frame)
                dialog.single_input_dialog(dialog_prompt)
                dialog.wait_window()  # This will wait until the dialog is destroyed
                values = dialog.result

                # If the user cancelled the dialog box, return
                if values is None:
                    return
            else:
                # Display a dialog box to request multiple values
                dialog = Dialog(parent_frame)
                dialog.multi_input_dialog()
                dialog.wait_window()  # This will wait until the dialog is destroyed
                values = dialog.result

                # If the user cancelled the dialog box, return
                if values is None:
                    return

            # If options is 1, call the remove function with a single argument
            # Otherwise, unpack the values and pass them as arguments
            if option == 1:
                removed = remove_func(values)
            else:
                removed = remove_func(*values)

            # If the item was successfully removed
            if removed is True:
                # If an item was selected, delete it from the tree
                if selected_items:
                    self.tree.delete(selected_items)
                else:
                    # If no item was selected, find and delete the item from the tree
                    for item in self.tree.get_children():
                        # Get the first value of the item
                        tree_id = str(self.tree.item(item)["values"][0]).strip()
                        tree_code = str(self.tree.item(item)["values"][1]).strip()

                        # If option is 1, compare the first value
                        if option == 1:
                            if tree_id == values:
                                self.tree.delete(item)
                                break
                            elif tree_code == values:
                                self.tree.delete(item)
                                break
                        else:
                            # Otherwise, compare all the values
                            tree_mod = str(self.tree.item(item)["values"][1]).strip()
                            tree_sem = str(self.tree.item(item)["values"][3]).strip()

                            if tree_id == values[0] and tree_mod == values[1] and tree_sem == values[2]:
                                self.tree.delete(item)
                                break
            else:
                # Display an error message
                messagebox.showerror("Error", "Failed to remove record.")

        # Update the record count
        match remove_func:
            case db_manager.remove_student:
                self.refresh(parent_frame, db_manager.get_students)
            case db_manager.remove_module:
                self.refresh(parent_frame, db_manager.get_modules)
            case db_manager.remove_details:
                self.refresh(parent_frame, db_manager.get_details)

        # Refresh the tree view
        self.tree.update_idletasks()

    def remove_student(self):
        self.remove_item(db_manager.remove_student, self.student_frame, dialog_prompt="Student ID:")

    def remove_module(self):
        self.remove_item(db_manager.remove_module, self.module_frame, dialog_prompt="Module:")

    def remove_details(self):
        self.remove_item(db_manager.remove_details, self.details_frame, 2)

    def update_search(self):
        # Update search function whenever search text is changed
        self.search_bar.bind('<KeyRelease>',
                             lambda event: self.helpers.search(self.tree, self.data, self.search_bar.get()))
