import tkinter as tk
from tkinter import messagebox, ttk

from database.queries import DatabaseManager
from gui.dialogs import Dialog
from gui.helpers import Helpers

db_manager = DatabaseManager()  # create an instance of DatabaseManager
global student_count  # keep track of the number of student records
global module_count  # keep track of the number of module records
global details_count  # keep track of the number of details records
global staff_count  # keep track of the number of staff records
global programme_count  # keep track of the number of programme records
global faculty_count  # keep track of the number of faculty records
global school_count  # keep track of the number of school records


class Views(ttk.Frame):

    def __init__(self, parent, master):
        super().__init__(parent)
        self._master = master
        self._width = self._master.winfo_width()
        self._height = self._master.winfo_height()
        self._original_width = 1330  # define the original screen width
        self._table_height = int(
            (self._height / 900) * (24 if self._height <= 768 else 27))  # Calculate table height based on window size
        self._search_bar = None
        self._data = None
        self._tree = None
        self._record_count_label = None
        self._student_frame = None
        self._details_frame = None
        self._module_frame = None
        self._faculty_frame = None
        self._staff_frame = None
        self._school_frame = None
        self._programme_frame = None
        self._helpers = Helpers()  # create an instance of Helpers
        self._parent = parent
        self._record_count_var = tk.StringVar()

    def create_view_frame(self):
        # Create frame
        frame = ttk.Frame(self._parent)
        frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Labels
        self._record_count_var.set(f"Number of Records: {len(self._data)}")
        self._record_count_label = ttk.Label(frame, textvariable=self._record_count_var)
        self._record_count_label.pack(side="top", pady=(10, 0))

        # Create search bar
        self._search_bar = self._helpers.create_search_bar(frame)

        return frame

    def create_view_table(self, frame, columns, column_widths, column_alignments, update_func, delete_func, data):
        # Calculate padding
        padx = self._width - sum(column_widths) - 52
        padx = 0 if padx < 0 else padx

        # Create Treeview
        tree = self._helpers.create_view_table(frame, columns, column_widths, column_alignments,
                                               update_func,
                                               delete_func,
                                               data=data,
                                               height=self._table_height,
                                               pad_x=padx)

        # Update search function whenever search text is changed
        self._update_search()

        # Pack the tree
        tree.grid(padx=10)

        return tree

    # View functions
    def student_view(self):
        # Get data
        self._data = db_manager.get_students()

        # Create student frame
        self._student_frame = self.create_view_frame()

        # Define columns
        columns = ("ID", "Student Name", "Student Email", "School", "Programme", "Advisor")
        column_widths = [int(self._width * (50 / self._original_width)),
                         int(self._width * (150 / self._original_width)),
                         int(self._width * (250 / self._original_width)),
                         int(self._width * (380 / self._original_width)),
                         int(self._width * (300 / self._original_width)),
                         int(self._width * (150 / self._original_width))]
        column_alignments = ["center", "w", "w", "w", "w", "w"]

        # Create Treeview
        self._tree = self.create_view_table(self._student_frame, columns, column_widths, column_alignments,
                                            self._update_student,
                                            self._delete_student,
                                            data=self._data)

        # Button configurations
        self._helpers.create_crud_buttons(self._student_frame, self._tree, db_manager.get_students, self._add_student,
                                          self._update_student,
                                          self._delete_student,
                                          self._refresh)

        return self._student_frame

    def module_view(self):
        # Get data
        self._data = db_manager.get_modules()

        # Create module frame
        self._module_frame = self.create_view_frame()

        # Define columns
        columns = ("Module Code", "Module Name", "Accreditation")
        column_widths = [int(self._width * (200 / self._original_width)),
                         int(self._width * (400 / self._original_width)),
                         int(self._width * (150 / self._original_width))]
        column_alignments = ["center", "w", "center"]

        # Create Treeview
        self._tree = self.create_view_table(self._module_frame, columns, column_widths, column_alignments,
                                            self._update_module,
                                            self._delete_module,
                                            data=self._data)

        # Button configurations
        self._helpers.create_crud_buttons(self._module_frame, self._tree, db_manager.get_modules, self._add_module,
                                          self._update_module,
                                          self._delete_module, self._refresh)

        return self._module_frame

    def details_view(self):
        # Get data
        self._data = db_manager.get_details()

        # Create details frame
        self._details_frame = self.create_view_frame()

        # Define columns
        columns = ("Student ID", "Module", "Grade Point Average", "Semester", "Year")
        column_widths = [int(self._width * (100 / self._original_width)),
                         int(self._width * (250 / self._original_width)),
                         int(self._width * (200 / self._original_width)),
                         int(self._width * (150 / self._original_width)),
                         int(self._width * (150 / self._original_width))]
        column_alignments = ["center", "w", "center", "center", "center"]

        # Create Treeview
        self._tree = self.create_view_table(self._details_frame, columns, column_widths, column_alignments,
                                            self._update_details,
                                            self._delete_details,
                                            data=self._data)

        # Button configurations
        self._helpers.create_crud_buttons(self._details_frame, self._tree, db_manager.get_details, self._add_details,
                                          self._update_details,
                                          self._delete_details, self._refresh)

        return self._details_frame

    def staff_view(self):
        # Get data
        self._data = db_manager.get_staff()

        # Create staff frame
        self._staff_frame = self.create_view_frame()

        # Define columns
        columns = ("Staff ID", "Name", "Email", "Position")
        column_widths = [int(self._width * (100 / self._original_width)),
                         int(self._width * (200 / self._original_width)),
                         int(self._width * (300 / self._original_width)),
                         int(self._width * (200 / self._original_width))]
        column_alignments = ["center", "w", "w", "w"]

        # Create Treeview
        self._tree = self.create_view_table(self._staff_frame, columns, column_widths, column_alignments,
                                            self._update_staff,
                                            self._delete_staff,
                                            data=self._data)

        # Button configurations
        self._helpers.create_crud_buttons(self._staff_frame, self._tree, db_manager.get_staff, self._add_staff,
                                          self._update_staff,
                                          self._delete_staff, self._refresh)

        return self._staff_frame

    def faculty_view(self):
        # Get data
        self._data = db_manager.get_faculties()

        # Create faculty frame
        self._faculty_frame = self.create_view_frame()

        # Define columns
        columns = ("Faculty Code", "Faculty Name", "Administrator")
        column_widths = [int(self._width * (200 / self._original_width)),
                         int(self._width * (450 / self._original_width)),
                         int(self._width * (250 / self._original_width))]
        column_alignments = ["center", "w", "w"]

        # Create Treeview
        self._tree = self.create_view_table(self._faculty_frame, columns, column_widths, column_alignments,
                                            self._update_faculty,
                                            self._delete_faculty,
                                            data=self._data)

        # Button configurations
        self._helpers.create_crud_buttons(self._faculty_frame, self._tree, db_manager.get_faculties, self._add_faculty,
                                          self._update_faculty,
                                          self._delete_faculty, self._refresh)

        return self._faculty_frame

    def school_view(self):
        # Get data
        self._data = db_manager.get_schools()

        # Create school frame
        self._school_frame = self.create_view_frame()

        # Define columns
        columns = ("School Code", "School Name", "Faculty", "Administrator")
        column_widths = [int(self._width * (200 / self._original_width)),
                         int(self._width * (430 / self._original_width)),
                         int(self._width * (450 / self._original_width)),
                         int(self._width * (200 / self._original_width))]
        column_alignments = ["center", "w", "w", "w"]

        # Create Treeview
        self._tree = self.create_view_table(self._school_frame, columns, column_widths, column_alignments,
                                            self._update_school,
                                            self._delete_school,
                                            data=self._data)

        # Button configurations
        self._helpers.create_crud_buttons(self._school_frame, self._tree, db_manager.get_schools, self._add_school,
                                          self._update_school,
                                          self._delete_school, self._refresh)

        return self._school_frame

    def programme_view(self):
        # Get data
        self._data = db_manager.get_programmes()

        # Create programme frame
        self._programme_frame = self.create_view_frame()

        # Define columns
        columns = ("Programme Code", "Programme Name", "School", "Director")
        column_widths = [int(self._width * (200 / self._original_width)),
                         int(self._width * (350 / self._original_width)),
                         int(self._width * (450 / self._original_width)),
                         int(self._width * (200 / self._original_width))]
        column_alignments = ["center", "w", "w", "w"]

        # Create Treeview
        self._tree = self.create_view_table(self._programme_frame, columns, column_widths, column_alignments,
                                            self._update_programme,
                                            self._delete_programme,
                                            data=self._data)

        # Button configurations
        self._helpers.create_crud_buttons(self._programme_frame, self._tree, db_manager.get_programmes,
                                          self._add_programme,
                                          self._update_programme,
                                          self._delete_programme, self._refresh)

        return self._programme_frame

    def __create_dialog(self, dialog_type, db_action, destroy=False, selected_item=None):
        # Create an instance of Dialog
        dialog = Dialog(self)
        fields = []  # Create an empty list to store the fields

        if dialog_type == "student":
            def submit_action():
                self._helpers.validate({"ID Number": (id_field, "int"),
                                        "Full Name": (name_field, "str"),
                                        "Email": (email_field, "email"),
                                        "School": (school_field, "str"),
                                        "Programme": (programme_field, "str"),
                                        "Advisor": (advisor_field, "str")}, db_action, dialog, destroy)

            if selected_item is not None:
                title = "Update Student"
            else:
                title = "Add Student"
            frame, id_field, name_field, email_field, school_field, programme_field, advisor_field \
                = dialog.student_dialog(title, submit_action)
            fields = [id_field, name_field, email_field, school_field, programme_field, advisor_field]
        elif dialog_type == "module":
            def submit_action():
                self._helpers.validate({
                    "Module Code": (code_field, "str"),
                    "Module Name": (name_field, "str"),
                    "Credits": (credits_field, "int")
                }, db_action, dialog, destroy)

            if selected_item is not None:
                title = "Update Module"
            else:
                title = "Add Module"
            frame, code_field, name_field, credits_field = dialog.module_dialog(title, submit_action)
            fields = [code_field, name_field, credits_field]
        elif dialog_type == "details":
            def submit_action():
                self._helpers.validate({
                    "ID Number": (id_field, "int"),
                    "Module": (module_field, "str"),
                    "GPA": (gpa_field, "float"),
                    "Semester": (semester_field, "int"),
                    "Year": (year_field, "str")
                }, db_action, dialog, destroy)

            if selected_item is not None:
                title = "Update Details"
            else:
                title = "Add Details"
            frame, id_field, module_field, gpa_field, semester_field, year_field, year_var \
                = dialog.details_dialog(title, submit_action)
            fields = [id_field, module_field, gpa_field, semester_field, year_field, year_var]
        elif dialog_type == "staff":
            def submit_action():
                self._helpers.validate({
                    "ID Number": (id_field, "int"),
                    "Name": (name_field, "str"),
                    "Email": (email_field, "email"),
                    "Position": (position_field, "str"),
                    "Username": (username_field, "username"),
                    "Password": (password_field, "password")
                }, db_action, dialog, destroy)

            if selected_item is not None:
                title = "Update Staff"
            else:
                title = "Add Staff"
            frame, id_field, name_field, email_field, position_field, username_field, password_field \
                = dialog.staff_dialog(title, submit_action)
            fields = [id_field, name_field, email_field, position_field, username_field, password_field]
        elif dialog_type == "faculty":
            def submit_action():
                self._helpers.validate({
                    "Code": (code_field, "str"),
                    "Name": (name_field, "str"),
                    "Administrator": (admin_field, "str")
                }, db_action, dialog, destroy)

            if selected_item is not None:
                title = "Update Faculty"
            else:
                title = "Add Faculty"
            frame, code_field, name_field, admin_field \
                = dialog.faculty_dialog(title, submit_action)
            fields = [code_field, name_field, admin_field]
        elif dialog_type == "school":
            def submit_action():
                self._helpers.validate({
                    "Code": (code_field, "str"),
                    "Name": (name_field, "str"),
                    "Faculty": (faculty_field, "str")
                }, db_action, dialog, destroy)

            if selected_item is not None:
                title = "Update School"
            else:
                title = "Add School"
            frame, code_field, name_field, faculty_field \
                = dialog.school_dialog(title, submit_action)
            fields = [code_field, name_field, faculty_field]
        elif dialog_type == "programme":
            def submit_action():
                self._helpers.validate({
                    "Code": (code_field, "str"),
                    "Name": (name_field, "str"),
                    "School": (school_field, "str"),
                    "Director": (director_field, "str")
                }, db_action, dialog, destroy)

            if selected_item is not None:
                title = "Update Programme"
            else:
                title = "Add Programme"
            frame, code_field, name_field, school_field, director_field \
                = dialog.programme_dialog(title, submit_action)
            fields = [code_field, name_field, school_field, director_field]

        if selected_item is not None:
            for i, field in enumerate(fields):
                values = self._tree.item(selected_item)["values"]
                if i < len(values):
                    if hasattr(field, 'set'):
                        field.set(str(values[i]).strip())
                    else:
                        field.insert(0, str(values[i]).strip())
                    if i == 0 and dialog_type != "details":
                        field.configure(state="disabled")
                    elif i < 2 and dialog_type == "details":  # ID and Module fields are disabled for updates
                        field.configure(state="disabled")

        dialog.wait_window()  # This will wait until the dialog is destroyed

    def _add_student(self):
        # Call the dialog box with no arguments
        self.__create_dialog("student", self._add_student_to_db)

    def _update_student(self):
        # Get the selected item from the tree
        selected_item = self._tree.selection()
        # Call the dialog box with the selected item
        self.__create_dialog("student", self._update_student_in_db, True, selected_item)

    def _add_module(self):
        # Call the dialog box with no arguments
        self.__create_dialog("module", self._add_module_to_db)

    def _update_module(self):
        # Get the selected item from the tree
        selected_item = self._tree.selection()
        # Call the dialog box with the selected item
        self.__create_dialog("module", self._update_module_in_db, True, selected_item)

    def _add_details(self):
        self.__create_dialog("details", self._add_detail_to_db)

    def _update_details(self):
        # Get the selected item from the tree
        selected_item = self._tree.selection()
        # Call the dialog box with the selected item
        self.__create_dialog("details", self._update_detail_in_db, True, selected_item)

    def _add_staff(self):
        self.__create_dialog("staff", self._add_staff_to_db)

    def _update_staff(self):
        # Get the selected item from the tree
        selected_item = self._tree.selection()
        # Call the dialog box with the selected item
        self.__create_dialog("staff", self._update_staff_in_db, True, selected_item)

    def _add_faculty(self):
        self.__create_dialog("faculty", self._add_faculty_to_db)

    def _update_faculty(self):
        # Get the selected item from the tree
        selected_item = self._tree.selection()
        # Call the dialog box with the selected item
        self.__create_dialog("faculty", self._update_faculty_in_db, True, selected_item)

    def _add_school(self):
        self.__create_dialog("school", self._add_school_to_db)

    def _update_school(self):
        # Get the selected item from the tree
        selected_item = self._tree.selection()
        # Call the dialog box with the selected item
        self.__create_dialog("school", self._update_school_in_db, True, selected_item)

    def _add_programme(self):
        self.__create_dialog("programme", self._add_programme_to_db)

    def _update_programme(self):
        # Get the selected item from the tree
        selected_item = self._tree.selection()
        # Call the dialog box with the selected item
        self.__create_dialog("programme", self._update_programme_in_db, True, selected_item)

    # Refresh functions
    def _refresh(self, frame, get_data_func):
        # Clear the tree
        self._tree.delete(*self._tree.get_children())

        # Get data
        self._data = get_data_func()

        match get_data_func:
            case db_manager.get_students:
                global student_count
                student_count = len(self._data)
                record_count = student_count
            case db_manager.get_details:
                global details_count
                details_count = len(self._data)
                record_count = details_count
            case db_manager.get_modules:
                global module_count
                module_count = len(self._data)
                record_count = module_count
            case db_manager.get_staff:
                global staff_count
                staff_count = len(self._data)
                record_count = staff_count
            case db_manager.get_faculties:
                global faculty_count
                faculty_count = len(self._data)
                record_count = faculty_count
            case db_manager.get_schools:
                global school_count
                school_count = len(self._data)
                record_count = school_count
            case db_manager.get_programmes:
                global programme_count
                programme_count = len(self._data)
                record_count = programme_count

        # Update the record count
        frame.after(100, lambda: self._record_count_var.set(f"Number of Records: {record_count}"))

        # Insert data in table
        for item in self._data:
            self._tree.insert("", "end", values=item)

        # Update the tree view
        self._tree.update_idletasks()

    def _add_to_db(self, add_record, data, success_message, error_message):
        # Insert the record into the database
        success = add_record(*data)
        if success:
            # Display a success message
            messagebox.showinfo("Success", success_message)
            match add_record:
                case db_manager.insert_student:
                    self._refresh(self._student_frame, db_manager.get_students)
                case db_manager.insert_detail:
                    self._refresh(self._details_frame, db_manager.get_details)
                case db_manager.insert_module:
                    self._refresh(self._module_frame, db_manager.get_modules)
                case db_manager.insert_staff:
                    self._refresh(self._staff_frame, db_manager.get_staff)
                case db_manager.insert_faculty:
                    self._refresh(self._faculty_frame, db_manager.get_faculties)
                case db_manager.insert_school:
                    self._refresh(self._school_frame, db_manager.get_schools)
                case db_manager.insert_programme:
                    self._refresh(self._programme_frame, db_manager.get_programmes)
        else:
            # Display an error message
            messagebox.showerror("Error", error_message)

        return success

    def _update_in_db(self, data, table_name, success_message, error_message):
        # Insert the record into the database
        success = db_manager.update_record(data, table_name)
        if success:
            # Display a success message
            messagebox.showinfo("Success", success_message)
            match table_name:
                case "student":
                    self._refresh(self._student_frame, db_manager.get_students)
                case "details":
                    self._refresh(self._details_frame, db_manager.get_details)
                case "module":
                    self._refresh(self._module_frame, db_manager.get_modules)
                case "staff":
                    self._refresh(self._staff_frame, db_manager.get_staff)
                case "faculty":
                    self._refresh(self._faculty_frame, db_manager.get_faculties)
                case "school":
                    self._refresh(self._school_frame, db_manager.get_schools)
                case "programme":
                    self._refresh(self._programme_frame, db_manager.get_programmes)
        else:
            # Display an error message
            messagebox.showerror("Error", error_message)

        return success

    # Add functions
    def _add_student_to_db(self, validated_fields):
        return self._add_to_db(db_manager.insert_student, (validated_fields["ID Number"], validated_fields["Full Name"],
                                                           validated_fields["Email"], validated_fields["School"],
                                                           validated_fields["Programme"], validated_fields["Advisor"]),
                               "Student record added successfully.",
                               "Failed to add student record.")

    def _add_module_to_db(self, validated_fields):
        return self._add_to_db(db_manager.insert_module,
                               (validated_fields["Module Code"], validated_fields["Module Name"],
                                validated_fields["Credits"]),
                               "Module record added successfully.",
                               "Failed to add module record.")

    def _add_detail_to_db(self, validated_fields):
        return self._add_to_db(db_manager.insert_detail, (validated_fields["ID Number"], validated_fields["Module"],
                                                          validated_fields["GPA"], validated_fields["Semester"],
                                                          validated_fields["Year"]),
                               "Detail record added successfully.",
                               "Failed to add detail record.")

    def _add_staff_to_db(self, validated_fields):
        return self._add_to_db(db_manager.insert_staff, (validated_fields["ID Number"], validated_fields["Name"],
                                                         validated_fields["Email"], validated_fields["Position"],
                                                         validated_fields["Username"], validated_fields["Password"]),
                               "Staff record added successfully.",
                               "Failed to add staff record.")

    def _add_faculty_to_db(self, validated_fields):
        return self._add_to_db(db_manager.insert_faculty, (validated_fields["Code"], validated_fields["Name"],
                                                           validated_fields["Administrator"]),
                               "Faculty record added successfully.",
                               "Failed to add faculty record.")

    def _add_school_to_db(self, validated_fields):
        return self._add_to_db(db_manager.insert_school, (validated_fields["Code"], validated_fields["Name"],
                                                          validated_fields["Faculty"]),
                               "School record added successfully.",
                               "Failed to add school record.")

    def _add_programme_to_db(self, validated_fields):
        return self._add_to_db(db_manager.insert_programme,
                               (validated_fields["Code"], validated_fields["Name"], validated_fields["School"],
                                validated_fields["Director"],),
                               "Programme record added successfully.",
                               "Failed to add programme record.")

    # Update functions
    def _update_student_in_db(self, validated_fields):
        return self._update_in_db((validated_fields["ID Number"], validated_fields["Full Name"],
                                   validated_fields["Email"], validated_fields["School"],
                                   validated_fields["Programme"], validated_fields["Advisor"]),
                                  "student",
                                  "Student record updated successfully.",
                                  "Failed to update student record.")

    def _update_detail_in_db(self, validated_fields):
        return self._update_in_db((validated_fields["ID Number"], validated_fields["Module"],
                                   validated_fields["GPA"], validated_fields["Semester"], validated_fields["Year"]),
                                  "details",
                                  "Module detail record updated successfully.",
                                  "Failed to update module detail record.")

    def _update_module_in_db(self, validated_fields):
        return self._update_in_db((validated_fields["Module Code"], validated_fields["Module Name"],
                                   validated_fields["Credits"]),
                                  "module",
                                  "Module record updated successfully.",
                                  "Failed to update module record.")

    def _update_staff_in_db(self, validated_fields):
        return self._update_in_db((validated_fields["ID Number"], validated_fields["Name"],
                                   validated_fields["Email"], validated_fields["Position"],
                                   validated_fields["Username"], validated_fields["Password"]),
                                  "staff",
                                  "Staff record updated successfully.",
                                  "Failed to update staff record.")

    def _update_faculty_in_db(self, validated_fields):
        return self._update_in_db((validated_fields["Code"], validated_fields["Name"],
                                   validated_fields["Administrator"]),
                                  "faculty",
                                  "Faculty record updated successfully.",
                                  "Failed to update faculty record.")

    def _update_school_in_db(self, validated_fields):
        return self._update_in_db((validated_fields["Code"], validated_fields["Name"],
                                   validated_fields["Faculty"]),
                                  "school",
                                  "School record updated successfully.",
                                  "Failed to update school record.")

    def _update_programme_in_db(self, validated_fields):
        return self._update_in_db((validated_fields["Code"], validated_fields["Name"],
                                   validated_fields["School"], validated_fields["Director"]),
                                  "programme",
                                  "Programme record updated successfully.",
                                  "Failed to update programme record.")

    # Delete functions
    def _delete_item(self, delete_func, parent_frame, option=1, get_func=None, get_id=True, dialog_prompt=None):
        # Get the selected item from the tree
        selected_items = self._tree.selection()

        # If an item is selected, get its values
        if selected_items:
            if messagebox.askokcancel("Confirm", "Are you sure you want to delete the selected item(s)?"):
                for selected_item in selected_items:
                    # If fields is None, get the first value
                    if option == 1:
                        values = str(self._tree.item(selected_item)["values"][0]).strip()
                        # Call the delete function with the appropriate arguments
                        deleted = delete_func(values)
                    else:
                        # Otherwise, get all the values
                        student_id = str(self._tree.item(selected_item)["values"][0]).strip()
                        module_code = str(self._tree.item(selected_item)["values"][1]).strip()
                        semester = str(self._tree.item(selected_item)["values"][3]).strip()
                        year = str(self._tree.item(selected_item)["values"][4]).strip()
                        values = [student_id, module_code, semester, year]
                        # Call the delete function with the appropriate arguments
                        deleted = delete_func(*values)

                    # If the item was successfully deleted, delete it from the tree
                    if deleted is True:
                        self._tree.delete(selected_item)
                    else:
                        # Display an error message
                        messagebox.showerror("Error", "Failed to delete record.")
            else:
                return
        else:
            # If no item is selected, display a dialog box to request the values
            if option == 1:
                # Display a dialog box to request a single value
                dialog = Dialog(parent_frame)
                dialog.single_input_dialog(dialog_prompt, get_func, get_id)
                dialog.wait_window()  # This will wait until the dialog is destroyed
                values = dialog.result

                # If the user cancelled the dialog box, return
                if values is None:
                    return

                # Call the delete function with the appropriate arguments
                deleted = delete_func(values)
            else:
                # Display a dialog box to request multiple values
                dialog = Dialog(parent_frame)
                dialog.multi_input_dialog()
                dialog.wait_window()  # This will wait until the dialog is destroyed
                values = dialog.result

                # If the user cancelled the dialog box, return
                if values is None:
                    return

                # Call the delete function with the appropriate arguments
                deleted = delete_func(*values)

            # If the item was successfully deleted
            if deleted is True:
                # If an item was selected, delete it from the tree
                if selected_items:
                    self._tree.delete(selected_items)
                else:
                    # If no item was selected, find and delete the item from the tree
                    for item in self._tree.get_children():
                        # Get the first value of the item
                        tree_id = str(self._tree.item(item)["values"][0]).strip()
                        tree_code = str(self._tree.item(item)["values"][1]).strip()

                        # If option is 1, compare the first value
                        if option == 1:
                            if tree_id == values:
                                self._tree.delete(item)
                                break
                            elif tree_code == values:
                                self._tree.delete(item)
                                break
                        else:
                            # Otherwise, compare all the values
                            tree_mod = str(self._tree.item(item)["values"][1]).strip()
                            tree_sem = str(self._tree.item(item)["values"][3]).strip()

                            if tree_id == values[0] and tree_mod == values[1] and tree_sem == values[2]:
                                self._tree.delete(item)
                                break
            else:
                # Display an error message
                messagebox.showerror("Error", "Failed to delete record.")

        # Update the record count
        match delete_func:
            case db_manager.delete_student:
                self._refresh(parent_frame, db_manager.get_students)
            case db_manager.delete_module:
                self._refresh(parent_frame, db_manager.get_modules)
            case db_manager.delete_details:
                self._refresh(parent_frame, db_manager.get_details)
            case db_manager.delete_staff:
                self._refresh(parent_frame, db_manager.get_staff)
            case db_manager.delete_faculty:
                self._refresh(parent_frame, db_manager.get_faculties)
            case db_manager.delete_school:
                self._refresh(parent_frame, db_manager.get_schools)
            case db_manager.delete_programme:
                self._refresh(parent_frame, db_manager.get_programmes)

        # Refresh the tree view
        self._tree.update_idletasks()

    def _delete_student(self):
        self._delete_item(db_manager.delete_student, self._student_frame, dialog_prompt="Student ID",
                          get_func=db_manager.get_students)

    def _delete_module(self):
        self._delete_item(db_manager.delete_module, self._module_frame, dialog_prompt="Module",
                          get_func=db_manager.get_modules, get_id=False)

    def _delete_details(self):
        self._delete_item(db_manager.delete_details, self._details_frame, 2)

    def _delete_staff(self):
        self._delete_item(db_manager.delete_staff, self._staff_frame, dialog_prompt="Staff ID",
                          get_func=db_manager.get_staff)

    def _delete_faculty(self):
        self._delete_item(db_manager.delete_faculty, self._faculty_frame, dialog_prompt="Faculty",
                          get_func=db_manager.get_faculties, get_id=False)

    def _delete_school(self):
        self._delete_item(db_manager.delete_school, self._school_frame, dialog_prompt="School",
                          get_func=db_manager.get_schools, get_id=False)

    def _delete_programme(self):
        self._delete_item(db_manager.delete_programme, self._programme_frame, dialog_prompt="Programme",
                          get_func=db_manager.get_programmes, get_id=False)

    def _update_search(self):
        # Update search function whenever search text is changed
        self._search_bar.bind('<KeyRelease>',
                              lambda event: self._helpers.search(self._tree, self._data, self._search_bar.get()))
