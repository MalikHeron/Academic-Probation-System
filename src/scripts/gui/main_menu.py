import tkinter as tk
from tkinter import messagebox, ttk

from scripts.database.queries import DatabaseManager
from scripts.gui.dialogs import Dialog
from scripts.gui.helpers import create_treeview, button_config, validate

db_manager = DatabaseManager()  # create an instance of DatabaseManager
global record_count  # global variable to keep track of the number of records


class Screens(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.record_count_label = None
        self.report_frame = None
        self.generate_report_button = None
        self.view_details_button = None
        self.student_frame = None
        self.details_frame = None
        self.module_frame = None
        self.view_modules_button = None
        self.view_students_button = None
        self.title = None
        self.parent = parent
        self.record_count_var = tk.StringVar()

    # View functions
    def student_view(self):
        # Create student frame
        self.student_frame = ttk.Frame(self.parent)
        self.student_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Get data
        data = db_manager.get_students()

        # Set global record count
        global record_count
        record_count = len(data)

        # Labels
        self.record_count_var.set(f"Number of Records: {record_count}")
        self.record_count_label = ttk.Label(self.student_frame, textvariable=self.record_count_var)
        self.record_count_label.pack(side="top", pady=(10, 0))

        # Define columns
        columns = ("ID", "Student Name", "Student Email", "School", "Programme", "Advisor")
        column_widths = [50, 150, 250, 380, 300, 150]
        column_alignments = ["center", "w", "w", "w", "w", "w"]

        # Create Treeview
        tree = create_treeview(self.student_frame, columns, column_widths, column_alignments, 10, data=data)

        # Button configurations
        button_config(self.student_frame, tree, db_manager.get_students, self.add_student, self.update_student,
                      self.remove_student,
                      self.refresh)

        return self.student_frame

    def module_view(self):
        # Create module frame
        self.module_frame = ttk.Frame(self.parent)
        self.module_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Get data
        data = db_manager.get_modules()

        # Set global record count
        global record_count
        record_count = len(data)

        # Labels
        self.record_count_var.set(f"Number of Records: {record_count}")
        self.record_count_label = ttk.Label(self.module_frame, textvariable=self.record_count_var)
        self.record_count_label.pack(side="top", pady=(10, 0))

        # Define columns
        columns = ("Module Code", "Module Name", "Accreditation")
        column_widths = [200, 400, 150]
        column_alignments = ["center", "w", "center"]

        # Create Treeview
        tree = create_treeview(self.module_frame, columns, column_widths, column_alignments, 10, data=data, padx=530)

        # Button configurations
        button_config(self.module_frame, tree, db_manager.get_modules, self.add_module, self.update_module,
                      self.remove_module, self.refresh)

        return self.module_frame

    def details_view(self):
        # Create module frame
        self.details_frame = ttk.Frame(self.parent)
        self.details_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Get data
        data = db_manager.get_details()

        # Set global record count
        global record_count
        record_count = len(data)

        # Labels
        self.record_count_var.set(f"Number of Records: {record_count}")
        self.record_count_label = ttk.Label(self.details_frame, textvariable=self.record_count_var)
        self.record_count_label.pack(side="top", pady=(10, 0))

        # Define columns
        columns = ("Student ID", "Module", "Grade Point Average", "Semester", "Year")
        column_widths = [100, 250, 200, 150, 150]
        column_alignments = ["center", "w", "center", "center", "center"]

        # Create Treeview
        tree = create_treeview(self.details_frame, columns, column_widths, column_alignments, 10, data=data, padx=430)

        # Button configurations
        button_config(self.details_frame, tree, db_manager.get_details, self.add_details, self.update_details,
                      self.remove_details, self.refresh)

        return self.details_frame

    def add_student(self):
        # Define the submit action
        def submit_action():
            validate({"ID": (student_id_field, "int"),
                      "Full Name": (student_name_field, "str"),
                      "Email": (student_email_field, "str"),
                      "School": (school_field, "str"),
                      "Programme": (programme_field, "str"),
                      "Advisor": (advisor_field, "str")},
                     self.add_student_to_db)

        dialog = Dialog(self)  # Create an instance of Dialog
        # Create the student frame
        frame, student_id_field, student_name_field, student_email_field, school_field, programme_field, advisor_field \
            = dialog.student_dialog("Add Student", submit_action)
        dialog.wait_window()  # This will wait until the dialog is destroyed

    def update_student(self, tree):
        # Get the selected item from the tree
        selected_item = tree.selection()

        # Define the submit action
        def submit_action():
            validate({"ID": (student_id_field, "int"),
                      "Full Name": (student_name_field, "str"),
                      "Email": (student_email_field, "str"),
                      "School": (school_field, "str"),
                      "Programme": (programme_field, "str"),
                      "Advisor": (advisor_field, "str")},
                     self.update_student_in_db)

        dialog = Dialog(self)  # Create an instance of Dialog
        # Create the student frame
        frame, student_id_field, student_name_field, student_email_field, school_field, programme_field, advisor_field \
            = dialog.student_dialog("Update Student", submit_action)

        # Populate fields
        student_id_field.insert(0, str(tree.item(selected_item)["values"][0]).strip())
        student_id_field.configure(state="disabled")
        student_name_field.insert(0, str(tree.item(selected_item)["values"][1]).strip())
        student_email_field.insert(0, str(tree.item(selected_item)["values"][2]).strip())
        school_field.set(str(tree.item(selected_item)["values"][3]).strip())
        programme_field.set(str(tree.item(selected_item)["values"][4]).strip())
        advisor_field.set(str(tree.item(selected_item)["values"][5]).strip())

        dialog.wait_window()  # This will wait until the dialog is destroyed

    def add_details(self):
        # Define the submit action
        def submit_action():
            validate({
                "ID": (id_field, "int"),
                "Module": (module_field, "str"),
                "GPA": (gpa_field, "float"),
                "Semester": (semester_field, "int"),
                "Year": (year_field, "int")
            }, self.add_detail_to_db)

        dialog = Dialog(self)  # Create an instance of Dialog
        # Create the details frame
        frame, id_field, gpa_field, module_field, semester_field, year_field, year_var \
            = dialog.details_dialog("Add Details", submit_action)
        dialog.wait_window()  # This will wait until the dialog is destroyed

    def update_details(self, tree):
        # Get the selected item from the tree
        selected_item = tree.selection()

        # Define the submit action
        def submit_action():
            validate({
                "ID": (id_field, "int"),
                "Module": (module_field, "str"),
                "GPA": (gpa_field, "float"),
                "Semester": (semester_field, "int"),
                "Year": (year_field, "int")
            }, self.update_detail_in_db)

        dialog = Dialog(self)  # Create an instance of Dialog
        # Create the details frame
        frame, id_field, gpa_field, module_field, semester_field, year_field, year_var \
            = dialog.details_dialog("Update Details", submit_action)

        # Populate fields
        id_field.insert(0, str(tree.item(selected_item)["values"][0]).strip())
        id_field.configure(state="disabled")
        module_field.insert(0, str(tree.item(selected_item)["values"][1]).strip())
        module_field.configure(state="disabled")
        gpa_field.insert(0, str(tree.item(selected_item)["values"][2]).strip())
        semester_field.set(str(tree.item(selected_item)["values"][3]).strip())
        year_var.set(str(tree.item(selected_item)["values"][4]).strip())

        dialog.wait_window()  # This will wait until the dialog is destroyed

    def add_module(self):
        # Define the submit action
        def submit_action():
            validate({
                "Module Code": (mod_code_field, "str"),
                "Module Name": (mod_name_field, "str"),
                "Credits": (mod_credits_field, "int")
            }, self.add_module_to_db)

        dialog = Dialog(self)  # Create an instance of Dialog
        # Create the module frame
        frame, mod_code_field, mod_name_field, mod_credits_field = dialog.module_dialog("Add Module",
                                                                                        submit_action)
        dialog.wait_window()  # This will wait until the dialog is destroyed

    def update_module(self, tree):
        # Get the selected item from the tree
        selected_item = tree.selection()

        # Define the submit action
        def submit_action():
            validate({
                "Module Code": (mod_code_field, "str"),
                "Module Name": (mod_name_field, "str"),
                "Credits": (mod_credits_field, "int")
            }, self.update_module_in_db)

        dialog = Dialog(self)  # Create an instance of Dialog
        # Create the module frame
        frame, mod_code_field, mod_name_field, mod_credits_field \
            = dialog.module_dialog("Update Module", submit_action)

        # Populate fields
        mod_code_field.insert(0, str(tree.item(selected_item)["values"][0]).strip())
        mod_code_field.configure(state="disabled")
        mod_name_field.insert(0, str(tree.item(selected_item)["values"][1]).strip())
        mod_credits_field.set(str(tree.item(selected_item)["values"][2]).strip())

        dialog.wait_window()  # This will wait until the dialog is destroyed

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

    # Refresh function
    def refresh(self, frame, tree, get_data_func):
        # Clear the tree
        tree.delete(*tree.get_children())

        # Get data
        data = get_data_func()

        # Set global record count
        global record_count
        record_count = len(data)

        # Update the record count label
        self.record_count_label.config(foreground="green")
        self.record_count_var.set("Table updated")

        # Change the color and text back to normal after 1 second
        frame.after(1000, lambda: self.record_count_label.config(foreground="black"))
        frame.after(1000, lambda: self.record_count_var.set(f"Number of Records: {record_count}"))

        # Insert data in table
        for item in data:
            tree.insert("", "end", values=item)

        # Update the tree view
        tree.update_idletasks()

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
    def remove_item(self, tree, remove_func, parent_frame, option=1, dialog_prompt=None):
        # Set global record count
        global record_count

        # Get the selected item from the tree
        selected_item = tree.selection()

        # If an item is selected, get its values
        if selected_item:
            # If fields is None, get the first value
            if option == 1:
                values = str(tree.item(selected_item)["values"][0]).strip()
            else:
                # Otherwise, get all the values
                student_id = str(tree.item(selected_item)["values"][0]).strip()
                module_code = str(tree.item(selected_item)["values"][1]).strip()
                semester = str(tree.item(selected_item)["values"][3]).strip()
                values = [student_id, module_code, semester]
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
            if selected_item:
                tree.delete(selected_item)
            else:
                # If no item was selected, find and delete the item from the tree
                for item in tree.get_children():
                    # Get the first value of the item
                    tree_id = str(tree.item(item)["values"][0]).strip()
                    tree_code = str(tree.item(item)["values"][1]).strip()

                    # If option is 1, compare the first value
                    if option == 1:
                        if tree_id == values:
                            tree.delete(item)
                            break
                        elif tree_code == values:
                            tree.delete(item)
                            break
                    else:
                        # Otherwise, compare all the values
                        tree_mod = str(tree.item(item)["values"][1]).strip()
                        tree_sem = str(tree.item(item)["values"][3]).strip()

                        if tree_id == values[0] and tree_mod == values[1] and tree_sem == values[2]:
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
        self.remove_item(tree, db_manager.remove_student, self.student_frame, dialog_prompt="Student ID:")

    def remove_module(self, tree):
        self.remove_item(tree, db_manager.remove_module, self.module_frame, dialog_prompt="Module:")

    def remove_details(self, tree):
        self.remove_item(tree, db_manager.remove_details, self.details_frame, 2)
