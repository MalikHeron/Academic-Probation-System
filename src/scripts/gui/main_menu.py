from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

import easygui

from scripts.database.queries import DatabaseManager
from scripts.gui.generate_report import GenerateReportFrame
from scripts.gui.helpers import create_treeview, button_config, create_button, create_label_and_field, \
    create_button_widget

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
        self.generate_report_button = create_button(self, "Generate Report", lambda: GenerateReportFrame(self.parent),
                                                    bg_color='#936BE9')

    # View Frames
    def view_students(self):
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
        columns = ("Student ID", "Student Name", "Student Email", "School", "Programme")
        column_widths = [100, 150, 250, 230, 230]

        # Create Treeview
        tree = create_treeview(self.student_frame, columns, column_widths, 10, data=data)

        # Button configurations
        button_config(self.student_frame, tree, self.add_student, self.remove_student, self.close_view)

    def view_modules(self):
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
        tree = create_treeview(self.module_frame, columns, column_widths, 115, data=data)

        # Button configurations
        button_config(self.module_frame, tree, self.add_module, self.remove_module, self.close_view)

    def view_details(self):
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
        columns = ("Student ID", "Module Code", "Grade Point", "Semester", "Year")
        column_widths = [100, 200, 150, 150, 150]

        # Create Treeview
        tree = create_treeview(self.details_frame, columns, column_widths, 115, data=data)

        # Button configurations
        button_config(self.details_frame, tree, self.add_details, self.remove_details, self.close_view)

    # Insert Frames
    def add_student(self):
        # Close the existing frame
        self.close_view()

        # Create the student frame
        self.add_student_frame = tk.Frame(self.parent, padx=40, pady=20)
        self.add_student_frame.grid(row=0, column=1, sticky="nsew")

        # Padding and field dimensions
        x_padding, y_padding, f_width, f_height, l_width = 5, 20, 25, 2, 11

        # Labels
        tk.Label(self.add_student_frame, text="Add Student",
                 font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        # Student ID label and field
        student_id_field = create_label_and_field(self.add_student_frame, "ID Number", 2)

        # Student Name label and field
        student_name_field = create_label_and_field(self.add_student_frame, "Full Name", 3)

        # Student Email label and field
        student_email_field = create_label_and_field(self.add_student_frame, "Email", 4)

        # School label and field
        school_field = create_label_and_field(self.add_student_frame, "School", 5)

        # Programme label and field
        programme_field = create_label_and_field(self.add_student_frame, "Programme", 6)

        # Submit and Cancel buttons
        button_frame = tk.Frame(self.add_student_frame)
        button_frame.grid(row=7, column=0, columnspan=3, padx=x_padding, pady=y_padding)

        create_button_widget(button_frame, "Submit",
                             lambda: [self.add_student_to_db(student_id_field.get(),
                                                             student_name_field.get(),
                                                             student_email_field.get(),
                                                             school_field.get(),
                                                             programme_field.get()),
                                      # Clear input fields
                                      self.clear_fields(student_id_field,
                                                        student_name_field,
                                                        student_email_field,
                                                        school_field,
                                                        programme_field)])

        create_button_widget(button_frame, "Clear", lambda: self.clear_fields(student_id_field,
                                                                              student_name_field,
                                                                              student_email_field,
                                                                              school_field,
                                                                              programme_field))

        create_button_widget(button_frame, "Back", lambda: self.close_view())

    def add_details(self):  # Do not touch this method yet, needs to be optimized
        self.close_view()

        # Create details frame
        self.add_details_frame = tk.Frame(self.parent)
        self.add_details_frame.grid(row=0, column=1, sticky="nsew")

        # Padding
        x_padding, y_padding, f_width, f_height = 15, 20, 25, 2

        # Labels
        tk.Label(self.add_details_frame, text="University of Technology", font=("Helvetica", 14, "bold")).grid(row=0,
                                                                                                               column=0,
                                                                                                               columnspan=2,
                                                                                                               pady=15)
        tk.Label(self.add_details_frame, text="Student Module Details", font=("Helvetica", 12)).grid(row=1, column=0,
                                                                                                     columnspan=2,
                                                                                                     pady=5)

        # ID number label and field
        tk.Label(self.add_details_frame, text="ID number", font=("Helvetica", 12)).grid(row=2, column=0, padx=x_padding,
                                                                                        pady=y_padding)
        id_field = tk.Text(self.add_details_frame, font=("Helvetica", 12), width=f_width, height=f_height)
        id_field.grid(row=2, column=1)

        # Module label and field
        tk.Label(self.add_details_frame, text="Module", font=("Helvetica", 12)).grid(row=3, column=0, padx=x_padding,
                                                                                     pady=y_padding)
        module_list = db_manager.get_modules()
        module_codes = [module[0] for module in module_list]  # Extract module codes
        module_field = tk.StringVar(self.add_details_frame)
        module_field.set(module_codes[0])  # default value
        module_menu = tk.OptionMenu(self.add_details_frame, module_field, *module_codes)
        module_menu.config(width=20)
        module_menu.grid(row=3, column=1, padx=x_padding, pady=y_padding)

        # Grade Point label and field
        tk.Label(self.add_details_frame, text="Grade Point Average", font=("Helvetica", 12)).grid(row=4, column=0,
                                                                                                  padx=x_padding,
                                                                                                  pady=y_padding)
        gpa_field = tk.Text(self.add_details_frame, font=("Helvetica", 12), width=f_width, height=f_height)
        gpa_field.grid(row=4, column=1)

        # Semester label and field
        tk.Label(self.add_details_frame, text="Semester", font=("Helvetica", 12)).grid(row=5, column=0, padx=x_padding,
                                                                                       pady=y_padding)
        semester_list = [1, 2]
        semester_field = tk.StringVar(self.add_details_frame)
        semester_field.set(semester_list[0])  # default value
        semester_menu = tk.OptionMenu(self.add_details_frame, semester_field, *semester_list)
        semester_menu.config(width=20)
        semester_menu.grid(row=5, column=1, padx=x_padding, pady=y_padding)

        # Year label and field
        tk.Label(self.add_details_frame, text="Year", font=("Helvetica", 12)).grid(row=6, column=0, padx=x_padding,
                                                                                   pady=y_padding)
        current_year = datetime.now().year
        year_list = list(range(2016, current_year + 1))
        year_field = tk.StringVar(self.add_details_frame)
        year_field.set(year_list[0])
        year_menu = tk.OptionMenu(self.add_details_frame, year_field, *year_list)
        year_menu.config(width=20)
        year_menu.grid(row=6, column=1, padx=x_padding, pady=y_padding)

        # Submit and Cancel buttons
        button_frame = tk.Frame(self.add_details_frame)
        button_frame.grid(row=7, column=0, columnspan=3, padx=x_padding, pady=y_padding)
        submit_button = tk.Button(button_frame, text="Submit", font=("Helvetica", 12), width=10,
                                  command=lambda: self.validate_and_submit(id_field, module_field, gpa_field,
                                                                           semester_field, year_field))

        submit_button.pack(side="left", padx=x_padding, pady=y_padding, anchor='center')
        clear_button = tk.Button(button_frame, text="Clear", font=("Helvetica", 12), width=10,
                                 command=lambda: self.clear_fields(id_field, gpa_field, module_field, semester_field,
                                                                   year_field))

        clear_button.pack(side="left", padx=x_padding, pady=y_padding, anchor='center')
        back_button = tk.Button(button_frame, text="Back", font=("Helvetica", 12), width=10,
                                command=lambda: self.close_view())
        back_button.pack(side="left", padx=x_padding, pady=y_padding, anchor='center')

    def add_module(self):
        # Close the existing frame
        self.close_view()

        # Create the module frame
        self.add_module_frame = tk.Frame(self.parent, padx=40, pady=20)
        self.add_module_frame.grid(row=0, column=1, sticky="nsew")

        # Padding and field dimensions
        x_padding, y_padding, f_width, f_height, l_width = 5, 20, 25, 2, 11

        # Labels
        tk.Label(self.add_module_frame, text="Add Module",
                 font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        # Module Code label and field
        mod_code_field = create_label_and_field(self.add_module_frame, "Module Code", 2)

        # Module Name label and field
        mod_name_field = create_label_and_field(self.add_module_frame, "Module Name", 3)

        # Credits label and field
        tk.Label(self.add_module_frame, text="Credits", width=l_width, anchor="w",
                 font=("Helvetica", 12)).grid(row=4, column=0, padx=x_padding, pady=y_padding)
        mod_credits_field = ttk.Combobox(self.add_module_frame, font=("Helvetica", 12), state="readonly",
                                         values=["1", "2", "3", "4"], width=f_width-2)
        mod_credits_field.grid(row=4, column=1)

        # Submit and Cancel buttons
        button_frame = tk.Frame(self.add_module_frame)
        button_frame.grid(row=7, column=0, columnspan=3, padx=x_padding, pady=y_padding)

        create_button_widget(button_frame, "Submit",
                             lambda: [self.add_module_to_db(mod_code_field.get(),
                                                            mod_name_field.get(),
                                                            int(mod_credits_field.get())),
                                      # Clear input fields
                                      self.clear_fields(mod_code_field,
                                                        mod_name_field,
                                                        mod_credits_field)])

        create_button_widget(button_frame, "Clear", lambda: self.clear_fields(mod_code_field,
                                                                              mod_name_field,
                                                                              mod_credits_field))

        create_button_widget(button_frame, "Back", lambda: self.close_view())

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

    @staticmethod
    def add_to_db(add_record, data, success_message, error_message):
        # Insert the record into the database
        success = add_record(data)
        if success:
            # Display a success message
            messagebox.showinfo("Success", success_message)
        else:
            # Display an error message
            messagebox.showerror("Error", error_message)

    def add_student_to_db(self, student_id, name, email, school, programme):
        self.add_to_db(db_manager.add_student, (student_id, name, email, school, programme),
                       "Student record added successfully.", "Failed to add student record.")

    def add_module_to_db(self, mod_code, mod_name, mod_credits):
        self.add_to_db(db_manager.add_module, (mod_code, mod_name, mod_credits),
                       "Module record added successfully.", "Failed to add module record.")

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
                record_count -= 1
                # Update the record count label
                self.record_count_var.set(f"Number of Records: {record_count}")

            # Refresh the tree view
            tree.update_idletasks()
        else:
            # Display an error message
            messagebox.showerror("Error", "Failed to remove item.")

    def remove_student(self, tree):
        self.remove_item(tree, db_manager.remove_student, "Input", "Please enter the ID of the student to be deleted:",
                         self.student_frame)

    def remove_module(self, tree):
        self.remove_item(tree, db_manager.remove_module, "Input", "Please enter the code of the module to be deleted:",
                         self.module_frame)

    def remove_details(self, tree):
        self.remove_item(tree, db_manager.remove_details, "Input", "Enter values for the fields.", self.details_frame,
                         ["Student ID", "Module Code", "Semester"])

    #Do not touch this method
    def validate_and_submit(self, id_field, module_field, gpa_field, semester_field, year_field):
        try:
            # validate id
            try:
                id_number = int(id_field.get("1.0", "end"))
                if id_number < 0:
                    raise ValueError
            except ValueError:
                tk.messagebox.showerror("Error", "ID number must be a positive integer.")
                return

            # Validate GPA
            try:
                gpa = float(gpa_field.get("1.0", "end"))
                if gpa < 0 or gpa > 4:
                    raise ValueError
            except ValueError:
                tk.messagebox.showerror("Error", "GPA must be a decimal number between 0 and 4.")
                return

            module = str(module_field.get()).strip()
            semester = int(semester_field.get())
            year = int(year_field.get())

            # Create a tuple with the values
            details_list = db_manager.get_details()
            details_tuple = (id_number, module, gpa, semester, year)

            # Check if the record already exists in the database
            if details_tuple in details_list:
                print("found")
                tk.messagebox.showerror("Error", "Record already exists in the database.")
                return

            # Insert the new record
            db_manager.insert_detail(id_number, module, gpa, semester, year)
            print("Data submitted:", id_number, module, gpa, semester, year)

        except Exception as e:
            print("An error occurred in validating submissions:", e)

    def clear_fields(self, id_field, gpa_field, module_field, semester_field, year_field):
        # Clear all fields and set to default values
        id_field.delete(1.0, 'end')
        gpa_field.delete(1.0, 'end')
        module_field.set(db_manager.get_modules()[0][0])
        semester_field.set(1)
        year_field.set(list(range(2016, datetime.now().year + 1))[0])

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

        elif self.add_module_frame is not None:
            self.add_module_frame.grid_forget()
            self.add_module_frame = None

        elif self.add_details_frame is not None:
            self.add_details_frame.grid_forget()
            self.add_details_frame = None
            self.view_details()
